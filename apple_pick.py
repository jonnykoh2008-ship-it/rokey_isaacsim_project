"""
M0617 + Robotiq 3F 그리퍼 사과 수확 동작

실행:
    /home/rokey/isaacsim/python.sh apple_pick.py

헤드리스 점검:
    /home/rokey/isaacsim/python.sh apple_pick.py --headless --max-steps 300

동작 순서:
    현재 자세 -> 사과 앞 접근 -> 사과 중심 진입 -> 3F 그리퍼 닫기
    -> 접근축 기준 45도 회전(1초) -> 로봇 방향으로 당기기 -> 후퇴
    -> 수직 상승 -> 컨베이어 바깥쪽 경유 -> 하향 파지 자세 전환
    -> 컨베이어 시작점 상공 이동 -> 저속 하강 -> 사과 놓기 -> 수직 이탈

중요:
    * 이 코드는 기존 USD/URDF를 저장하거나 수정하지 않는다.
    * FixedJoint의 파손 한계 15 N / 0.6 N·m는 실행 중인 Stage에만 적용한다.
    * 15 N은 당기는 명령값이 아니라 Joint가 끊어지는 반력 한계다.
    * GUI에서 Stop 후 Play를 누르면 물리와 IK를 초기화하고 처음부터 재실행한다.
"""

import argparse
import traceback
from pathlib import Path

import numpy as np

from isaacsim import SimulationApp


# SimulationApp은 다른 Isaac Sim 모듈보다 먼저 생성해야 한다.
parser = argparse.ArgumentParser(description="M0617 3F apple picking")
parser.add_argument("--headless", action="store_true", help="화면 없이 실행")
parser.add_argument(
    "--max-steps",
    type=int,
    default=0,
    help="0이면 창을 닫을 때까지 실행, 양수이면 지정한 물리 스텝 뒤 종료",
)
args, _unknown = parser.parse_known_args()

simulation_app = SimulationApp(
    {
        "headless": args.headless,
        "sync_loads": True,
        "width": 1280,
        "height": 720,
    }
)

import omni.usd
from pxr import Gf, Usd, UsdGeom, UsdPhysics

from isaacsim.core.api import World
from isaacsim.core.utils.rotations import quat_to_rot_matrix, rot_matrix_to_quat
from isaacsim.core.utils.stage import is_stage_loading
from isaacsim.core.utils.types import ArticulationAction
from isaacsim.robot.manipulators.manipulators import SingleManipulator
from isaacsim.robot_motion.motion_generation import (
    ArticulationKinematicsSolver,
    LulaKinematicsSolver,
)


# ══════════════════════════════════════════════════════════════
# 파일과 Stage Prim 경로
# ══════════════════════════════════════════════════════════════
PROJECT_DIR = Path(__file__).resolve().parent
STAGE_PATH = PROJECT_DIR / "m0617_3fgripper08201638.usd"
DESCRIPTION_PATH = PROJECT_DIR / "m0617_robot_description.yaml"
URDF_PATH = (
    PROJECT_DIR
    / "m0617_gripper"
    / "dsr_description2"
    / "urdf"
    / "m0617.urdf"
)

ARTICULATION_PRIM_PATH = "/World/m0617_rail"
ARTICULATION_ROOT_JOINT_PATH = "/World/m0617_rail/root_joint"
ROBOT_MOUNT_JOINT_PATH = "/World/FixedJoint"
ROBOT_PRIM_PATH = "/World/m0617"
ROBOT_BASE_PATH = "/World/m0617/base_link"
LINK6_PATH = "/World/m0617/link_6"
GRIPPER_ROOT_PATH = "/World/m0617/robotiq_3f_gripper_articulated"
PALM_PATH = "/World/m0617/robotiq_3f_gripper_articulated/palm"
APPLE_PATH = "/World/Xform/applebody/apple1"
FIXED_JOINT_PATH = "/World/Xform/FixedJoint"
CONVEYOR_PATH = "/World/ConveyorBelt_A08_PR_NVD_01"
RUNTIME_CONVEYOR_COLLIDER_PATH = "/World/RuntimeConveyorBeltSurface"

EE_FRAME_NAME = "link_6"
RAIL_JOINT = "rail_joint"
ARM_JOINTS = [f"joint_{index}" for index in range(1, 7)]


# ══════════════════════════════════════════════════════════════
# 사과 분리와 이동 조건
# ══════════════════════════════════════════════════════════════
BREAK_FORCE_N = 15.0
BREAK_TORQUE_NM = 1.0

# 파지 중심은 Palm 로컬 +Y 방향 약 12.5 cm 지점이다.
# 세 distal link 원점의 배치를 기준으로 한 고정 TCP 근사값이다.
PALM_TO_TCP = np.array([0.0, 0.125, 0.0], dtype=float)

PREGRASP_DISTANCE_M = 0.15
PULL_DISTANCE_M = 0.10
RETREAT_DISTANCE_M = 0.25
RETREAT_HEIGHT_M = 0.15
TWIST_DEG = 45.0
TWIST_STEPS = 60  # Stage가 60 Hz일 때 약 1초

# 한 물리 스텝에서 TCP 목표가 이동하는 최대 거리이다.
TCP_STEP_M = 0.002
MIN_MOVE_STEPS = 90
MAX_MOVE_STEPS = 900

# 컨베이어 끝단 바로 위는 사과가 굴러 떨어질 수 있으므로 안쪽으로 배치한다.
# 사과를 든 상태에서는 상판 20 cm 위까지 이동한 뒤, 마지막 구간만 매우
# 천천히 내려 충격을 줄인다. RELEASE_CLEARANCE_M는 사과 바닥과 상판 사이의
# 작은 여유이며, 실제 접촉 후 그리퍼를 서서히 여는 동안 중력으로 안착한다.
CONVEYOR_END_INSET_M = 0.45
CONVEYOR_SIDE_INSET_M = 0.15
CONVEYOR_OUTSIDE_OFFSET_M = 0.30
SAFE_CARRY_CLEARANCE_M = 0.15
# 이 로봇 배치에서는 하향 그리퍼 자세로 상판 25 cm 위를 요구하면 손목이
# 작업반경을 벗어난다. 실제 IK 결과에서 LOWER는 성공했으므로 12 cm 상공에서
# 정렬한 뒤 저속 하강한다.
PLACE_APPROACH_HEIGHT_M = 0.12
# 손가락이 상판에 닿기 전에 사과를 놓는다. 사과는 약 2 cm만 자유낙하하므로
# 컨베이어와 직접 충돌하면서 억지로 밀어 넣는 것보다 충격이 작다.
RELEASE_CLEARANCE_M = 0.020
PLACE_TRANSIT_STEP_M = 0.0015
PLACE_DESCENT_STEP_M = 0.0005
PLACE_ROTATE_STEPS = 180
RELEASE_STEPS = 120
PLACE_LIFT_STEPS = 150
MAX_CONSECUTIVE_IK_FAILURES = 180
TARGET_POSITION_TOLERANCE_M = 0.025
TARGET_ORIENTATION_TOLERANCE_DEG = 6.0
MAX_TARGET_SETTLE_STEPS = 180
APPLE_GRASP_MAX_DISTANCE_M = 0.14

# 충돌 시 1e8 수준의 강한 Drive가 컨베이어를 억지로 뚫지 않도록 제한한다.
# M0617이 느린 보간 목표를 추종할 수 있는 범위에서 보수적으로 낮춘 값이다.
ARM_DRIVE_STIFFNESS = 1.0e6
ARM_DRIVE_DAMPING = 1.0e4
ARM_DRIVE_MAX_FORCE = 2.0e3

# 시작 자세에서 사과 앞까지는 매 프레임 Cartesian IK를 다시 풀지 않는다.
# 사과 앞 pregrasp 자세의 IK를 한 번만 구한 뒤, 현재 관절값과 가장 가까운
# 동치 각도를 선택하여 관절공간에서 부드럽게 이동한다.
JOINT_STEP_RAD = 0.006
MIN_JOINT_MOVE_STEPS = 120
MAX_JOINT_MOVE_STEPS = 900
JOINT_SETTLE_STEPS = 180
JOINT_SETTLE_TOLERANCE_RAD = 0.02

# m0617.urdf의 6축 관절 제한이다. ±2π 범위 관절에서 IK가 같은 자세를
# 반대쪽 회전값으로 반환해 불필요하게 한 바퀴 도는 현상을 막는 데 사용한다.
ARM_LOWER_LIMITS = np.array(
    [-6.2832, -6.2832, -2.8798, -6.2832, -6.2832, -6.2832],
    dtype=float,
)
ARM_UPPER_LIMITS = np.array(
    [6.2832, 6.2832, 2.8798, 6.2832, 6.2832, 6.2832],
    dtype=float,
)


# ══════════════════════════════════════════════════════════════
# 3F 그리퍼 관절
# ══════════════════════════════════════════════════════════════
# 이 3F 모델은 Mimic joint가 없으므로 11개 회전관절을 직접 동기화한다.
GRIPPER_JOINTS = [
    "palm_finger_1_joint",
    "finger_1_joint_1",
    "finger_1_joint_2",
    "finger_1_joint_3",
    "palm_finger_2_joint",
    "finger_2_joint_1",
    "finger_2_joint_2",
    "finger_2_joint_3",
    "finger_middle_joint_1",
    "finger_middle_joint_2",
    "finger_middle_joint_3",
]

# 열린 자세는 URDF의 모든 관절 0 rad이다.
GRIPPER_OPEN = np.zeros(len(GRIPPER_JOINTS), dtype=float)

# 약 10 cm 사과를 감싸기 위한 목표값이다. 충돌이 정상이라면 손가락은
# 사과 표면에서 멈추며, Drive가 이 목표를 계속 유지해 파지력을 만든다.
GRIPPER_CLOSED = np.array(
    [
        0.0,
        0.75,
        0.90,
        -0.55,
        0.0,
        0.75,
        0.90,
        -0.55,
        0.75,
        0.90,
        -0.55,
    ],
    dtype=float,
)


# ══════════════════════════════════════════════════════════════
# 작은 수학 유틸
# ══════════════════════════════════════════════════════════════
def normalized(vector):
    """벡터를 단위벡터로 만든다."""
    vector = np.asarray(vector, dtype=float)
    length = float(np.linalg.norm(vector))
    if length < 1e-9:
        raise ValueError("길이가 0인 벡터는 정규화할 수 없습니다.")
    return vector / length


def rotation_about_y(angle_rad):
    """로컬 Y축 회전행렬을 만든다."""
    c = np.cos(angle_rad)
    s = np.sin(angle_rad)
    return np.array([[c, 0.0, s], [0.0, 1.0, 0.0], [-s, 0.0, c]])


def slerp(q0, q1, alpha):
    """(w, x, y, z) 쿼터니언을 최단 경로로 보간한다."""
    q0 = normalized(q0)
    q1 = normalized(q1)
    dot = float(np.dot(q0, q1))

    if dot < 0.0:
        q1 = -q1
        dot = -dot

    if dot > 0.9995:
        return normalized(q0 + alpha * (q1 - q0))

    theta_0 = np.arccos(np.clip(dot, -1.0, 1.0))
    sin_theta_0 = np.sin(theta_0)
    theta = theta_0 * alpha
    return (
        np.sin(theta_0 - theta) / sin_theta_0 * q0
        + np.sin(theta) / sin_theta_0 * q1
    )


def smoothstep(alpha):
    """구간 시작과 끝에서 속도를 줄이는 3차 보간 함수다."""
    alpha = float(np.clip(alpha, 0.0, 1.0))
    return alpha * alpha * (3.0 - 2.0 * alpha)


def vec(vector, digits=4):
    return "[" + " ".join(f"{value:+.{digits}f}" for value in vector) + "]"


def gf_quat_to_numpy(quaternion):
    """Gf.Quat 계열을 Isaac 형식 (w, x, y, z) 배열로 바꾼다."""
    imaginary = quaternion.GetImaginary()
    return np.array(
        [quaternion.GetReal(), imaginary[0], imaginary[1], imaginary[2]],
        dtype=float,
    )


def get_prim_world_pose(stage, prim_path):
    """USD Prim의 현재 월드 위치와 회전을 Isaac 형식으로 반환한다."""
    transform = UsdGeom.XformCache(Usd.TimeCode.Default()).GetLocalToWorldTransform(
        require_prim(stage, prim_path)
    )
    return (
        np.asarray(transform.ExtractTranslation(), dtype=float),
        gf_quat_to_numpy(transform.ExtractRotationQuat()),
    )


# ══════════════════════════════════════════════════════════════
# Stage 검사와 물리 설정
# ══════════════════════════════════════════════════════════════
def require_prim(stage, prim_path):
    prim = stage.GetPrimAtPath(prim_path)
    if not prim.IsValid():
        raise RuntimeError(f"필수 Prim을 찾을 수 없습니다: {prim_path}")
    return prim


def validate_articulation_setup(stage):
    """레일과 M0617이 하나의 Articulation으로 연결됐는지 검사한다."""
    root_prim = require_prim(stage, ARTICULATION_ROOT_JOINT_PATH)
    if not root_prim.HasAPI(UsdPhysics.ArticulationRootAPI):
        raise RuntimeError(
            f"Articulation Root API가 없습니다: {ARTICULATION_ROOT_JOINT_PATH}"
        )

    root_joint = UsdPhysics.Joint(root_prim)
    if not root_joint.GetJointEnabledAttr().Get():
        raise RuntimeError(
            f"Articulation Root Joint가 비활성화되었습니다: "
            f"{ARTICULATION_ROOT_JOINT_PATH}"
        )

    mount_joint = UsdPhysics.Joint(require_prim(stage, ROBOT_MOUNT_JOINT_PATH))
    body0 = [str(path) for path in mount_joint.GetBody0Rel().GetTargets()]
    body1 = [str(path) for path in mount_joint.GetBody1Rel().GetTargets()]
    expected0 = ["/World/m0617_rail/rail_robot_mount_link"]
    expected1 = [ROBOT_BASE_PATH]
    if body0 != expected0 or body1 != expected1:
        raise RuntimeError(
            "레일-M0617 FixedJoint 대상이 예상과 다릅니다: "
            f"Body0={body0}, Body1={body1}"
        )


def open_project_stage():
    """저장된 조립 USD를 열고 모든 참조가 로드될 때까지 기다린다."""
    for path in (STAGE_PATH, DESCRIPTION_PATH, URDF_PATH):
        if not path.exists():
            raise FileNotFoundError(path)

    omni.usd.get_context().open_stage(str(STAGE_PATH))
    simulation_app.update()
    simulation_app.update()
    while is_stage_loading():
        simulation_app.update()

    stage = omni.usd.get_context().get_stage()
    for prim_path in (
        ARTICULATION_PRIM_PATH,
        ARTICULATION_ROOT_JOINT_PATH,
        ROBOT_PRIM_PATH,
        ROBOT_BASE_PATH,
        LINK6_PATH,
        PALM_PATH,
        APPLE_PATH,
        FIXED_JOINT_PATH,
        CONVEYOR_PATH,
    ):
        require_prim(stage, prim_path)

    validate_articulation_setup(stage)

    meters_per_unit = UsdGeom.GetStageMetersPerUnit(stage)
    if not np.isclose(meters_per_unit, 1.0):
        raise RuntimeError(f"Stage 단위가 meter가 아닙니다: {meters_per_unit}")

    print(f"   Stage        {STAGE_PATH}")
    print("   Stage units  1.0 meter")
    return stage


def configure_breakable_joint(stage):
    """사과-가지 FixedJoint의 연결과 파손 한계를 실행 Stage에 적용한다."""
    joint_prim = require_prim(stage, FIXED_JOINT_PATH)
    joint = UsdPhysics.Joint(joint_prim)

    body0 = [str(path) for path in joint.GetBody0Rel().GetTargets()]
    body1 = [str(path) for path in joint.GetBody1Rel().GetTargets()]
    expected0 = ["/World/Xform/branchbody"]
    expected1 = ["/World/Xform/applebody"]
    if body0 != expected0 or body1 != expected1:
        raise RuntimeError(
            "FixedJoint Body 대상이 예상과 다릅니다: "
            f"Body0={body0}, Body1={body1}"
        )

    joint.GetBreakForceAttr().Set(BREAK_FORCE_N)
    joint.GetBreakTorqueAttr().Set(BREAK_TORQUE_NM)
    joint.GetJointEnabledAttr().Set(True)
    joint.GetCollisionEnabledAttr().Set(False)

    print(
        f"   Apple joint  break force {BREAK_FORCE_N:.1f} N, "
        f"torque {BREAK_TORQUE_NM:.2f} N·m"
    )


def configure_joint_drives(stage):
    """팔은 위치를 잘 추종하고, 손가락은 과도한 충격 없이 닫히게 한다."""
    arm_count = 0
    gripper_count = 0
    root = require_prim(stage, ROBOT_PRIM_PATH)

    for prim in Usd.PrimRange(root):
        name = prim.GetName()
        drive = UsdPhysics.DriveAPI.Get(prim, "angular")
        if not drive:
            continue

        if name in ARM_JOINTS:
            drive.GetStiffnessAttr().Set(ARM_DRIVE_STIFFNESS)
            drive.GetDampingAttr().Set(ARM_DRIVE_DAMPING)
            drive.GetMaxForceAttr().Set(ARM_DRIVE_MAX_FORCE)
            arm_count += 1
        elif name in GRIPPER_JOINTS:
            drive.GetStiffnessAttr().Set(200.0)
            drive.GetDampingAttr().Set(20.0)
            drive.GetMaxForceAttr().Set(20.0)
            gripper_count += 1

    if arm_count != len(ARM_JOINTS):
        raise RuntimeError(f"팔 Drive 수가 잘못되었습니다: {arm_count}")
    if gripper_count != len(GRIPPER_JOINTS):
        raise RuntimeError(f"그리퍼 Drive 수가 잘못되었습니다: {gripper_count}")

    print(f"   Drives       arm {arm_count}, gripper {gripper_count}")


def configure_contact_colliders(stage):
    """3F 손가락과 사과가 실제로 충돌하도록 런타임 Collider를 구성한다.

    조립된 3F USD에는 충돌용 STL Mesh가 들어 있지만 instance proxy라서
    Collision API가 적용되어 있지 않다. Instance 내부에는 속성을 직접
    작성할 수 없으므로, 각 Rigid Body 링크의 로컬 좌표계로 충돌 Mesh를
    복제하고 convex hull Collider를 적용한다.

    이 변경은 메모리에서 열린 Stage에만 적용되며 원본 USD는 저장하지 않는다.
    """
    gripper_root = require_prim(stage, GRIPPER_ROOT_PATH)
    xform_cache = UsdGeom.XformCache(Usd.TimeCode.Default())
    collider_count = 0

    rigid_links = [
        prim
        for prim in Usd.PrimRange(gripper_root)
        if prim.HasAPI(UsdPhysics.RigidBodyAPI)
    ]

    for link_prim in rigid_links:
        # URDF의 <collision>에서 가져온 STL만 사용한다. Visual Mesh를
        # Collider로 사용하면 형상이 지나치게 복잡해질 수 있다.
        source_prim = next(
            (
                prim
                for prim in Usd.PrimRange(
                    link_prim,
                    Usd.TraverseInstanceProxies(),
                )
                if prim.IsA(UsdGeom.Mesh) and "/collisions/" in str(prim.GetPath())
            ),
            None,
        )
        if source_prim is None:
            raise RuntimeError(f"충돌 STL Mesh를 찾을 수 없습니다: {link_prim.GetPath()}")

        source_mesh = UsdGeom.Mesh(source_prim)
        source_points = source_mesh.GetPointsAttr().Get()
        face_counts = source_mesh.GetFaceVertexCountsAttr().Get()
        face_indices = source_mesh.GetFaceVertexIndicesAttr().Get()
        if not source_points or not face_counts or not face_indices:
            raise RuntimeError(f"충돌 STL Mesh 데이터가 비어 있습니다: {source_prim.GetPath()}")

        # Source Mesh의 점을 해당 Rigid Body 링크 로컬 좌표로 변환한다.
        source_to_world = xform_cache.GetLocalToWorldTransform(source_prim)
        world_to_link = xform_cache.GetLocalToWorldTransform(link_prim).GetInverse()
        link_points = []
        for point in source_points:
            world_point = source_to_world.Transform(Gf.Vec3d(point))
            link_point = world_to_link.Transform(world_point)
            link_points.append(Gf.Vec3f(link_point))

        collider_path = link_prim.GetPath().AppendChild("runtime_collision")
        if stage.GetPrimAtPath(collider_path).IsValid():
            stage.RemovePrim(collider_path)

        collider_mesh = UsdGeom.Mesh.Define(stage, collider_path)
        collider_mesh.CreatePointsAttr().Set(link_points)
        collider_mesh.CreateFaceVertexCountsAttr().Set(face_counts)
        collider_mesh.CreateFaceVertexIndicesAttr().Set(face_indices)
        collider_mesh.CreateSubdivisionSchemeAttr().Set(UsdGeom.Tokens.none)

        # 화면에는 원래 Visual Mesh만 보이고, PhysX에는 이 Mesh만 사용된다.
        collider_mesh.CreateVisibilityAttr().Set(UsdGeom.Tokens.invisible)
        collision = UsdPhysics.CollisionAPI.Apply(collider_mesh.GetPrim())
        collision.CreateCollisionEnabledAttr().Set(True)
        mesh_collision = UsdPhysics.MeshCollisionAPI.Apply(collider_mesh.GetPrim())
        mesh_collision.CreateApproximationAttr().Set("convexHull")
        collider_count += 1

    # 사과 Mesh에는 Collision API가 이미 있지만 저장된 USD에서 비활성화돼
    # 있으므로 활성화하고 동적 물체에 사용할 수 있는 convex hull로 고정한다.
    apple_root = require_prim(stage, APPLE_PATH)
    apple_collision_prims = [
        prim
        for prim in Usd.PrimRange(apple_root)
        if prim.IsA(UsdGeom.Mesh) and prim.HasAPI(UsdPhysics.CollisionAPI)
    ]
    if len(apple_collision_prims) != 1:
        raise RuntimeError(
            "사과 Collision Mesh 수가 예상과 다릅니다: "
            f"{len(apple_collision_prims)}"
        )

    apple_collision_prim = apple_collision_prims[0]
    apple_collision = UsdPhysics.CollisionAPI(apple_collision_prim)
    apple_collision.GetCollisionEnabledAttr().Set(True)
    apple_mesh_collision = UsdPhysics.MeshCollisionAPI.Apply(apple_collision_prim)
    apple_mesh_collision.CreateApproximationAttr().Set("convexHull")

    print(
        f"   Colliders    gripper {collider_count}, apple 1 "
        "(runtime convex hull)"
    )


def compute_apple_center(stage):
    """사과 피벗이 아니라 렌더 Mesh의 월드 Bounding Box 중심을 구한다."""
    apple = require_prim(stage, APPLE_PATH)
    bbox_cache = UsdGeom.BBoxCache(
        Usd.TimeCode.Default(),
        [UsdGeom.Tokens.default_, UsdGeom.Tokens.render, UsdGeom.Tokens.proxy],
        useExtentsHint=True,
    )
    box = bbox_cache.ComputeWorldBound(apple).ComputeAlignedBox()
    center = np.array(box.GetMidpoint(), dtype=float)
    size = np.array(box.GetSize(), dtype=float)
    print(f"   Apple center {vec(center)}")
    print(f"   Apple size   {vec(size)}")
    return center, size


def compute_conveyor_start(stage, robot_position, apple_size):
    """컨베이어 시작점과 그 바깥쪽의 안전 접근점을 계산한다.

    원격 컨베이어 자산에는 Collider가 없으므로 PhysX raycast를 사용할 수
    없다. 대신 payload 안의 Mesh별 월드 경계를 조사해 넓고 얇은 수평 Mesh를
    벨트 상판으로 선택한다. 선택된 경계로 실행 중에만 정적 상판 Collider를
    만들며 원본 USD에는 저장하지 않는다.
    """
    conveyor = require_prim(stage, CONVEYOR_PATH)
    bbox_cache = UsdGeom.BBoxCache(
        Usd.TimeCode.Default(),
        [UsdGeom.Tokens.default_, UsdGeom.Tokens.render, UsdGeom.Tokens.proxy],
        useExtentsHint=True,
    )
    root_box = bbox_cache.ComputeWorldBound(conveyor).ComputeAlignedBox()
    root_size = np.array(root_box.GetSize(), dtype=float)
    if not np.all(np.isfinite(root_size)) or np.any(root_size <= 1e-4):
        raise RuntimeError(
            "컨베이어 payload가 로드되지 않아 크기를 계산할 수 없습니다. "
            "인터넷 연결 또는 NVIDIA 자산 캐시를 확인하세요."
        )

    surface_candidates = []
    for prim in Usd.PrimRange(conveyor, Usd.TraverseInstanceProxies()):
        if not prim.IsA(UsdGeom.Mesh):
            continue
        mesh_box = bbox_cache.ComputeWorldBound(prim).ComputeAlignedBox()
        mesh_size = np.array(mesh_box.GetSize(), dtype=float)
        if not np.all(np.isfinite(mesh_size)) or np.any(mesh_size[:2] <= 0.05):
            continue
        horizontal_area = float(mesh_size[0] * mesh_size[1])
        thickness = max(float(mesh_size[2]), 0.01)
        score = horizontal_area / thickness
        if "belt" in prim.GetName().lower():
            score *= 4.0
        surface_candidates.append((score, prim, mesh_box, mesh_size))

    if surface_candidates:
        _score, surface_prim, box, _surface_size = max(
            surface_candidates,
            key=lambda item: item[0],
        )
        surface_path = str(surface_prim.GetPath())
    else:
        # 자산이 하나의 결합 Mesh인 경우에만 전체 경계를 최후 수단으로 쓴다.
        box = root_box
        surface_path = f"{CONVEYOR_PATH} (combined fallback)"

    minimum = np.array(box.GetMin(), dtype=float)
    maximum = np.array(box.GetMax(), dtype=float)
    size = maximum - minimum

    center = 0.5 * (minimum + maximum)
    travel_axis = int(np.argmax(size[:2]))
    side_axis = 1 - travel_axis
    inset = min(CONVEYOR_END_INSET_M, 0.25 * size[travel_axis])

    negative_end = center.copy()
    positive_end = center.copy()
    negative_end[travel_axis] = minimum[travel_axis] + inset
    positive_end[travel_axis] = maximum[travel_axis] - inset
    robot_xy = np.asarray(robot_position[:2], dtype=float)
    candidates = (negative_end, positive_end)
    start = min(
        candidates,
        key=lambda point: np.linalg.norm(point[:2] - robot_xy),
    ).copy()

    # 폭 중앙은 로봇에서 불필요하게 멀 수 있다. 사과가 가장자리에서 떨어지지
    # 않을 만큼만 안쪽으로 들어간, 로봇과 가까운 폭 좌표를 사용한다.
    side_inset = min(CONVEYOR_SIDE_INSET_M, 0.25 * size[side_axis])
    start[side_axis] = np.clip(
        robot_xy[side_axis],
        minimum[side_axis] + side_inset,
        maximum[side_axis] - side_inset,
    )

    # 경유점은 벨트 진행축 끝 너머가 아니라 로봇과 가까운 측면 바깥에 둔다.
    # 이렇게 해야 팔이 먼 끝으로 우회하지 않고 컨베이어를 가로지르지도 않는다.
    outside_direction = np.zeros(3, dtype=float)
    outside_direction[side_axis] = np.sign(robot_xy[side_axis] - center[side_axis])
    if abs(outside_direction[side_axis]) < 0.5:
        distance_to_min = abs(robot_xy[side_axis] - minimum[side_axis])
        distance_to_max = abs(robot_xy[side_axis] - maximum[side_axis])
        outside_direction[side_axis] = -1.0 if distance_to_min <= distance_to_max else 1.0
    if abs(outside_direction[side_axis]) < 0.5:
        raise RuntimeError("컨베이어 바깥쪽 방향을 결정하지 못했습니다.")
    outside = start.copy()
    outside[side_axis] = (
        minimum[side_axis] - CONVEYOR_OUTSIDE_OFFSET_M
        if outside_direction[side_axis] < 0.0
        else maximum[side_axis] + CONVEYOR_OUTSIDE_OFFSET_M
    )

    # 배치 자세의 수평축은 선택한 시작 끝에서 벨트 중심으로 향하게 한다.
    conveyor_direction = np.zeros(3, dtype=float)
    conveyor_direction[travel_axis] = -np.sign(
        start[travel_axis] - center[travel_axis]
    )

    surface_z = float(maximum[2])

    # 사과가 시각 Mesh를 통과하지 않도록 벨트 경계와 같은 크기의 얇은 정적
    # Cube Collider를 만든다. 프로그램을 다시 실행하면 기존 Prim을 교체한다.
    runtime_path = RUNTIME_CONVEYOR_COLLIDER_PATH
    if stage.GetPrimAtPath(runtime_path).IsValid():
        stage.RemovePrim(runtime_path)
    collider_thickness = max(0.04, min(float(size[2]), 0.10))
    collider_center = 0.5 * (minimum + maximum)
    collider_center[2] = surface_z - 0.5 * collider_thickness
    collider_size = np.array([size[0], size[1], collider_thickness], dtype=float)
    collider_cube = UsdGeom.Cube.Define(stage, runtime_path)
    collider_cube.CreateSizeAttr(1.0)
    collider_xform = UsdGeom.Xformable(collider_cube.GetPrim())
    collider_xform.AddTranslateOp().Set(
        Gf.Vec3d(*(float(value) for value in collider_center))
    )
    collider_xform.AddScaleOp().Set(
        Gf.Vec3f(*(float(value) for value in collider_size))
    )
    collider_cube.CreateVisibilityAttr().Set(UsdGeom.Tokens.invisible)
    collision = UsdPhysics.CollisionAPI.Apply(collider_cube.GetPrim())
    collision.CreateCollisionEnabledAttr().Set(True)

    # TCP가 사과 중심에 위치하므로, 사과 반높이와 작은 낙하 여유를 더한다.
    start[2] = surface_z + 0.5 * apple_size[2] + RELEASE_CLEARANCE_M
    outside[2] = start[2]
    axis_name = "X" if travel_axis == 0 else "Y"
    print(f"   Conveyor     surface mesh {surface_path}")
    print(f"   Conveyor     surface bbox min {vec(minimum)}, max {vec(maximum)}")
    print(
        f"   Conveyor     runtime collider {runtime_path}, "
        f"size {vec(collider_size)}"
    )
    print(f"   Conveyor     travel axis {axis_name}, start {vec(start)}")
    print(f"   Conveyor     outside waypoint {vec(outside)}")
    return start, outside, surface_z, conveyor_direction


def compute_link6_to_palm(stage):
    """조립된 USD에서 link_6 -> palm 고정변환을 읽는다."""
    cache = UsdGeom.XformCache(Usd.TimeCode.Default())
    link_matrix = cache.GetLocalToWorldTransform(require_prim(stage, LINK6_PATH))
    palm_matrix = cache.GetLocalToWorldTransform(require_prim(stage, PALM_PATH))

    link_position = np.array(link_matrix.ExtractTranslation(), dtype=float)
    palm_position = np.array(palm_matrix.ExtractTranslation(), dtype=float)
    link_quat = gf_quat_to_numpy(link_matrix.ExtractRotationQuat())
    palm_quat = gf_quat_to_numpy(palm_matrix.ExtractRotationQuat())
    link_rotation = quat_to_rot_matrix(link_quat)
    palm_rotation = quat_to_rot_matrix(palm_quat)

    rotation = link_rotation.T @ palm_rotation
    translation = link_rotation.T @ (palm_position - link_position)
    print(f"   Palm offset  translation {vec(translation)}")
    return translation, rotation


# ══════════════════════════════════════════════════════════════
# TCP, Palm, link_6 변환
# ══════════════════════════════════════════════════════════════
def make_approach_rotation(robot_position, apple_position):
    """Palm 로컬 +Y가 로봇에서 사과로 향하도록 수평 접근 자세를 만든다."""
    forward = np.array(
        [
            apple_position[0] - robot_position[0],
            apple_position[1] - robot_position[1],
            0.0,
        ]
    )
    y_axis = normalized(forward)
    z_axis = np.array([0.0, 0.0, 1.0])
    x_axis = normalized(np.cross(y_axis, z_axis))
    return np.column_stack((x_axis, y_axis, z_axis)), y_axis


def make_downward_place_rotation(horizontal_hint):
    """Palm의 접근축(+Y)이 아래를 향하는 컨베이어 배치 자세를 만든다.

    그리퍼가 수평인 채 하강하면 손가락 끝이 상판을 긁을 수 있다. +Y축을
    월드 -Z로 두고, 기존 접근 방향을 수평 X축 힌트로 사용해 급격한 yaw
    변화를 줄인 오른손 좌표계를 구성한다.
    """
    x_axis = np.asarray(horizontal_hint, dtype=float).copy()
    x_axis[2] = 0.0
    x_axis = normalized(x_axis)
    y_axis = np.array([0.0, 0.0, -1.0])
    z_axis = normalized(np.cross(x_axis, y_axis))
    return np.column_stack((x_axis, y_axis, z_axis))


def tcp_target_to_link6(
    tcp_position,
    palm_rotation,
    link6_to_palm_translation,
    link6_to_palm_rotation,
):
    """원하는 파지 중심 자세를 Lula가 계산할 link_6 목표로 변환한다."""
    palm_position = tcp_position - palm_rotation @ PALM_TO_TCP
    link_rotation = palm_rotation @ link6_to_palm_rotation.T
    link_position = palm_position - link_rotation @ link6_to_palm_translation
    return link_position, rot_matrix_to_quat(link_rotation)


def current_tcp_pose(robot):
    """현재 Palm pose에서 파지 중심의 월드 pose를 계산한다."""
    palm_position, palm_quat = robot.end_effector.get_world_pose()
    palm_rotation = quat_to_rot_matrix(palm_quat)
    tcp_position = palm_position + palm_rotation @ PALM_TO_TCP
    return np.asarray(tcp_position), palm_rotation


def rotation_error_deg(actual_rotation, target_rotation):
    """두 회전행렬 사이의 최소 회전각을 degree로 반환한다."""
    relative = np.asarray(target_rotation).T @ np.asarray(actual_rotation)
    cosine = np.clip((np.trace(relative) - 1.0) * 0.5, -1.0, 1.0)
    return float(np.rad2deg(np.arccos(cosine)))


# ══════════════════════════════════════════════════════════════
# 수확 상태 기계
# ══════════════════════════════════════════════════════════════
class AppleHarvestFSM:
    """사과 접근부터 수확 후 컨베이어에 내려놓기까지 연속 동작을 만든다."""

    NAMES = [
        "APPROACH",
        "ENTER",
        "GRASP",
        "TWIST",
        "PULL",
        "RETREAT",
        "CLEAR_UP",
        "OUTSIDE",
        "ALIGN",
        "TO_BELT",
        "RELEASE",
        "LIFT",
        "DONE",
    ]

    def __init__(
        self,
        current_tcp,
        current_palm_rotation,
        apple_center,
        approach_rotation,
        approach_direction,
        conveyor_start,
        conveyor_outside,
        conveyor_top_z,
        conveyor_direction,
        start_at_pregrasp=False,
    ):
        self.apple_center = np.asarray(apple_center, dtype=float)
        self.approach_rotation = np.asarray(approach_rotation, dtype=float)
        self.approach_direction = np.asarray(approach_direction, dtype=float)
        self.twisted_rotation = approach_rotation @ rotation_about_y(np.deg2rad(TWIST_DEG))
        # 손가락 방향을 벨트 긴 축과 맞춰 폭 방향 난간과의 간섭을 줄인다.
        self.place_rotation = make_downward_place_rotation(conveyor_direction)

        pregrasp = apple_center - approach_direction * PREGRASP_DISTANCE_M
        pull = apple_center - approach_direction * PULL_DISTANCE_M
        retreat = (
            apple_center
            - approach_direction * RETREAT_DISTANCE_M
            + np.array([0.0, 0.0, RETREAT_HEIGHT_M])
        )
        place = np.asarray(conveyor_start, dtype=float)
        outside = np.asarray(conveyor_outside, dtype=float)
        place_above = place + np.array([0.0, 0.0, PLACE_APPROACH_HEIGHT_M])
        safe_z = max(
            retreat[2] + SAFE_CARRY_CLEARANCE_M,
            float(conveyor_top_z) + SAFE_CARRY_CLEARANCE_M,
            place_above[2],
        )
        clear_up = retreat.copy()
        clear_up[2] = safe_z
        outside_safe = outside.copy()
        # 측면 경유점까지 같은 최고 높이를 유지하면 수평거리와 높이가 동시에
        # 커져 작업반경을 벗어난다. 컨베이어 바깥에서 상판보다 충분히 높은
        # 수준으로 낮춘 뒤 자세를 전환한다.
        outside_safe[2] = min(
            safe_z,
            place_above[2],
        )
        # 같은 X/Y에서 수직 상승하는 자세는 IK가 실패했다. 사과를 놓은 뒤
        # 도달 가능성이 확인된 측면 경유점으로 비스듬히 빠져나간다.
        place_lift = outside_safe.copy()

        approach_steps = int(
            np.clip(
                np.linalg.norm(pregrasp - current_tcp) / TCP_STEP_M,
                MIN_MOVE_STEPS,
                MAX_MOVE_STEPS,
            )
        )

        specs = [
            (pregrasp, approach_rotation, approach_steps, 0.0, 0.0),
            (apple_center, approach_rotation, 100, 0.0, 0.0),
            (apple_center, approach_rotation, 120, 0.0, 1.0),
            (apple_center, self.twisted_rotation, TWIST_STEPS, 1.0, 1.0),
            (pull, self.twisted_rotation, 120, 1.0, 1.0),
            (retreat, self.twisted_rotation, 180, 1.0, 1.0),
            (
                clear_up,
                self.twisted_rotation,
                max(120, int(np.ceil(np.linalg.norm(clear_up - retreat) / PLACE_TRANSIT_STEP_M))),
                1.0,
                1.0,
            ),
            (
                outside_safe,
                self.twisted_rotation,
                max(
                    MIN_MOVE_STEPS,
                    int(np.ceil(np.linalg.norm(outside_safe - clear_up) / PLACE_TRANSIT_STEP_M)),
                ),
                1.0,
                1.0,
            ),
            # 컨베이어에서 떨어진 높은 위치에서만 그리퍼를 아래로 돌린다.
            (outside_safe, self.place_rotation, PLACE_ROTATE_STEPS, 1.0, 1.0),
            (
                place,
                self.place_rotation,
                max(
                    MIN_MOVE_STEPS,
                    int(
                        np.ceil(
                            np.linalg.norm(place - outside_safe)
                            / PLACE_DESCENT_STEP_M
                        )
                    ),
                ),
                1.0,
                1.0,
            ),
            (place, self.place_rotation, RELEASE_STEPS, 1.0, 0.0),
            (place_lift, self.place_rotation, PLACE_LIFT_STEPS, 0.0, 0.0),
        ]

        names = self.NAMES[:-1]
        if start_at_pregrasp:
            # pregrasp까지의 장거리 이동은 관절공간 이동 함수가 담당했다.
            # 여기서는 사과 중심으로 들어가는 짧은 Cartesian 구간부터 시작한다.
            specs = specs[1:]
            names = names[1:]

        self.specs = specs
        self.NAMES = names + ["DONE"]

        self.state = 0
        self.frame = 0
        self.settle_frame = 0
        self.start_position = np.asarray(current_tcp, dtype=float)
        self.start_quat = rot_matrix_to_quat(current_palm_rotation)
        self._print_state()

    @property
    def done(self):
        return self.state >= len(self.specs)

    def _print_state(self):
        if self.done:
            print("   [DONE] 사과 수확 궤적 완료")
            return
        goal_position, _rotation, steps, _grip0, grip1 = self.specs[self.state]
        print(
            f"   [{self.NAMES[self.state]:8s}] goal {vec(goal_position)} "
            f"steps {steps:3d}, grip {grip1:.1f}"
        )
        if self.NAMES[self.state] == "ALIGN":
            palm_forward = self.place_rotation[:, 1]
            palm_side = self.place_rotation[:, 0]
            print(
                f"   [ALIGN   ] Palm +Y(접근축) {vec(palm_forward)}, "
                f"belt axis {vec(palm_side)}"
            )

    def sample(self):
        """현재 프레임의 TCP pose와 그리퍼 닫힘 비율을 반환한다."""
        if self.done:
            goal_position, goal_rotation, _steps, _g0, _g1 = self.specs[-1]
            return goal_position, goal_rotation, 1.0

        goal_position, goal_rotation, steps, grip0, grip1 = self.specs[self.state]
        alpha = min(1.0, (self.frame + 1) / float(steps))
        move_alpha = smoothstep(alpha)
        position = self.start_position + move_alpha * (goal_position - self.start_position)
        goal_quat = rot_matrix_to_quat(goal_rotation)
        orientation = quat_to_rot_matrix(slerp(self.start_quat, goal_quat, alpha))
        grip = grip0 + smoothstep(alpha) * (grip1 - grip0)
        return position, orientation, grip

    def advance(self, actual_position, actual_rotation):
        """명령 시간과 실제 TCP 도달 조건을 모두 만족할 때만 다음 단계로 간다."""
        if self.done:
            return "done"

        goal_position, goal_rotation, steps, _grip0, _grip1 = self.specs[self.state]
        if self.frame < steps:
            self.frame += 1
        if self.frame < steps:
            return "moving"

        position_error = float(np.linalg.norm(goal_position - actual_position))
        orientation_error = rotation_error_deg(actual_rotation, goal_rotation)
        if (
            position_error > TARGET_POSITION_TOLERANCE_M
            or orientation_error > TARGET_ORIENTATION_TOLERANCE_DEG
        ):
            self.settle_frame += 1
            if self.settle_frame == 1 or self.settle_frame % 60 == 0:
                print(
                    f"   [{self.NAMES[self.state]:8s}] 도달 대기 "
                    f"position {position_error:.4f} m, "
                    f"rotation {orientation_error:.2f} deg"
                )
            if self.settle_frame >= MAX_TARGET_SETTLE_STEPS:
                return "timeout"
            return "waiting"

        self.start_position = np.asarray(goal_position, dtype=float)
        self.start_quat = rot_matrix_to_quat(goal_rotation)
        self.state += 1
        self.frame = 0
        self.settle_frame = 0
        self._print_state()
        return "advanced"


# ══════════════════════════════════════════════════════════════
# 로봇과 IK 초기화
# ══════════════════════════════════════════════════════════════
def create_robot(world):
    """레일, M0617, 3F 그리퍼로 연결된 단일 Articulation을 등록한다."""
    robot = world.scene.add(
        SingleManipulator(
            prim_path=ARTICULATION_PRIM_PATH,
            end_effector_prim_path=PALM_PATH,
            name="m0617_3f_robot",
            gripper=None,
        )
    )
    # world.reset()이 Scene에 등록된 Articulation과 end-effector를 함께
    # 초기화한다. 여기서 robot.initialize()를 다시 호출하면 PhysX view가
    # 중복 생성되어 non-root link 관련 경고가 발생할 수 있다.
    world.reset()

    required_joints = [RAIL_JOINT] + ARM_JOINTS + GRIPPER_JOINTS
    missing = [name for name in required_joints if name not in robot.dof_names]
    if missing:
        raise RuntimeError(f"Articulation에서 관절을 찾을 수 없습니다: {missing}")

    print(f"   Articulation {robot.num_dof} DOF")
    for index, name in enumerate(robot.dof_names):
        if name == RAIL_JOINT:
            group = "rail"
        elif name in ARM_JOINTS:
            group = "arm"
        elif name in GRIPPER_JOINTS:
            group = "3f"
        else:
            group = "other"
        print(f"      [{index:2d}] {name:28s} {group}")
    return robot


def create_ik_solver(robot, stage):
    """M0617 6축만 제어하는 Lula IK를 만든다."""
    lula = LulaKinematicsSolver(
        robot_description_path=str(DESCRIPTION_PATH),
        urdf_path=str(URDF_PATH),
    )
    # Articulation의 루트는 레일이므로 robot.get_world_pose()를 쓰면 Lula의
    # 기준이 레일 원점으로 잘못 설정된다. 실제 M0617 base_link pose를 쓴다.
    base_position, base_orientation = get_prim_world_pose(stage, ROBOT_BASE_PATH)
    lula.set_robot_base_pose(
        robot_position=np.asarray(base_position),
        robot_orientation=np.asarray(base_orientation),
    )
    print(f"   Robot base   {vec(base_position)}")
    print(f"   Lula joints  {', '.join(lula.get_joint_names())}")
    articulation_solver = ArticulationKinematicsSolver(
        robot_articulation=robot,
        kinematics_solver=lula,
        end_effector_frame_name=EE_FRAME_NAME,
    )
    return articulation_solver, lula


def apply_gripper_target(robot, gripper_indices, close_ratio):
    """0.0=open, 1.0=closed 비율로 11개 그리퍼 관절을 명령한다."""
    targets = GRIPPER_OPEN + close_ratio * (GRIPPER_CLOSED - GRIPPER_OPEN)
    robot.apply_action(
        ArticulationAction(
            joint_positions=targets,
            joint_indices=np.asarray(gripper_indices, dtype=np.int32),
        )
    )


def nearest_equivalent_joint_goal(current_positions, solved_positions):
    """각 관절 제한 안에서 현재 각도와 가장 가까운 2π 동치 목표를 고른다."""
    current_positions = np.asarray(current_positions, dtype=float)
    solved_positions = np.asarray(solved_positions, dtype=float)
    if current_positions.shape != (len(ARM_JOINTS),):
        raise RuntimeError(f"현재 팔 관절 배열 크기가 잘못되었습니다: {current_positions.shape}")
    if solved_positions.shape != (len(ARM_JOINTS),):
        raise RuntimeError(f"IK 팔 관절 배열 크기가 잘못되었습니다: {solved_positions.shape}")

    adjusted = solved_positions.copy()
    period = 2.0 * np.pi
    for index, solved in enumerate(solved_positions):
        candidates = solved + period * np.arange(-2, 3, dtype=float)
        valid = candidates[
            (candidates >= ARM_LOWER_LIMITS[index] - 1e-6)
            & (candidates <= ARM_UPPER_LIMITS[index] + 1e-6)
        ]
        if valid.size:
            adjusted[index] = valid[np.argmin(np.abs(valid - current_positions[index]))]
    return adjusted


def move_arm_to_pregrasp(
    world,
    robot,
    ik_solver,
    gripper_indices,
    pregrasp_tcp,
    approach_rotation,
    link6_to_palm_translation,
    link6_to_palm_rotation,
    max_physics_steps=0,
):
    """pregrasp IK를 한 번 풀고, 가장 짧은 관절 경로로 목표까지 이동한다."""
    link_position, link_orientation = tcp_target_to_link6(
        pregrasp_tcp,
        approach_rotation,
        link6_to_palm_translation,
        link6_to_palm_rotation,
    )
    ik_action, solved = ik_solver.compute_inverse_kinematics(
        target_position=link_position,
        target_orientation=link_orientation,
        position_tolerance=0.003,
        orientation_tolerance=np.deg2rad(3.0),
    )
    if not solved:
        raise RuntimeError(f"pregrasp IK를 계산하지 못했습니다: TCP {vec(pregrasp_tcp)}")

    arm_subset = ik_solver.get_joints_subset()
    start_positions = np.asarray(arm_subset.get_joint_positions(), dtype=float)
    solved_positions = np.asarray(ik_action.joint_positions, dtype=float)
    goal_positions = nearest_equivalent_joint_goal(start_positions, solved_positions)
    joint_delta = goal_positions - start_positions

    move_steps = int(
        np.clip(
            np.ceil(np.max(np.abs(joint_delta)) / JOINT_STEP_RAD),
            MIN_JOINT_MOVE_STEPS,
            MAX_JOINT_MOVE_STEPS,
        )
    )

    print("   [TRANSIT ] 관절공간 최단 경로로 pregrasp 이동")
    print(f"   Arm start    {vec(start_positions, digits=3)}")
    print(f"   Arm goal     {vec(goal_positions, digits=3)}")
    print(f"   Arm delta    {vec(joint_delta, digits=3)}")
    print(f"   Transit      {move_steps} steps")

    physics_steps = 0
    for frame in range(move_steps):
        if not simulation_app.is_running():
            return physics_steps, False
        if max_physics_steps > 0 and physics_steps >= max_physics_steps:
            return physics_steps, False

        # Pause는 현재 보간 프레임을 유지한 채 기다리고, Stop은 PhysX
        # Articulation handle을 해제하므로 즉시 상위 재시작 루프로 돌아간다.
        while not world.is_playing():
            if world.is_stopped() or not simulation_app.is_running():
                return physics_steps, False
            world.step(render=not args.headless)

        alpha = smoothstep((frame + 1) / float(move_steps))
        command = start_positions + alpha * joint_delta
        arm_subset.apply_action(joint_positions=command)
        apply_gripper_target(robot, gripper_indices, 0.0)
        world.step(render=not args.headless)
        physics_steps += 1

        # UI 이벤트는 world.step() 안에서 처리된다. 그 호출 도중 Stop이 눌리면
        # 바로 아래의 관절 로그도 이미 해제된 handle을 읽게 되므로 재검사한다.
        if world.is_stopped():
            return physics_steps, False

        if frame == 0 or (frame + 1) % 60 == 0 or frame + 1 == move_steps:
            actual = np.asarray(arm_subset.get_joint_positions(), dtype=float)
            error = float(np.max(np.abs(goal_positions - actual)))
            print(
                f"   TRANSIT   {frame + 1:4d}/{move_steps:4d} "
                f"max joint error {error:.4f} rad"
            )

    # 보간 종료 뒤 Drive가 최종 목표에 도달할 시간을 준다.
    for _settle in range(JOINT_SETTLE_STEPS):
        while not world.is_playing():
            if world.is_stopped() or not simulation_app.is_running():
                return physics_steps, False
            world.step(render=not args.headless)

        actual = np.asarray(arm_subset.get_joint_positions(), dtype=float)
        error = float(np.max(np.abs(goal_positions - actual)))
        if error <= JOINT_SETTLE_TOLERANCE_RAD:
            actual_tcp, _actual_rotation = current_tcp_pose(robot)
            tcp_error = float(np.linalg.norm(pregrasp_tcp - actual_tcp))
            if tcp_error <= TARGET_POSITION_TOLERANCE_M:
                print(
                    f"   [TRANSIT ] 완료: joint error {error:.4f} rad, "
                    f"TCP error {tcp_error:.4f} m"
                )
                return physics_steps, True
            if _settle == 0 or (_settle + 1) % 60 == 0:
                print(
                    f"   [TRANSIT ] TCP 도달 대기: joint error {error:.4f} rad, "
                    f"TCP error {tcp_error:.4f} m"
                )

        if not simulation_app.is_running():
            return physics_steps, False
        if max_physics_steps > 0 and physics_steps >= max_physics_steps:
            return physics_steps, False

        arm_subset.apply_action(joint_positions=goal_positions)
        apply_gripper_target(robot, gripper_indices, 0.0)
        world.step(render=not args.headless)
        physics_steps += 1
        if world.is_stopped():
            return physics_steps, False

    actual = np.asarray(arm_subset.get_joint_positions(), dtype=float)
    error = float(np.max(np.abs(goal_positions - actual)))
    actual_tcp, _actual_rotation = current_tcp_pose(robot)
    tcp_error = float(np.linalg.norm(pregrasp_tcp - actual_tcp))
    print(
        f"   [TRANSIT ] 목표 수렴 실패: joint error {error:.4f} rad, "
        f"TCP error {tcp_error:.4f} m"
    )
    return physics_steps, False


def validate_planned_ik(
    fsm,
    lula_solver,
    initial_joint_positions,
    pregrasp_tcp,
    approach_rotation,
    link6_to_palm_translation,
    link6_to_palm_rotation,
):
    """로봇을 움직이기 전에 전체 경로를 순차 warm-start IK로 검사한다.

    각 목표를 홈 자세에서 독립적으로 풀면 실제 순차 경로가 가능한데도 실패할
    수 있다. 앞 목표의 관절 해를 다음 목표의 seed로 사용해 실제 FSM 순서를
    그대로 검사한다. ENTER도 포함하므로 사과 중심 진입 실패를 미리 발견한다.
    """
    planned_targets = [
        ("PREGRASP", (pregrasp_tcp, approach_rotation, 0, 0.0, 0.0)),
        *list(zip(fsm.NAMES, fsm.specs)),
    ]
    warm_start = np.asarray(initial_joint_positions, dtype=float)
    checked = 0
    for state_name, spec in planned_targets:
        target_tcp, target_rotation, _steps, _grip0, _grip1 = spec
        link_position, link_orientation = tcp_target_to_link6(
            target_tcp,
            target_rotation,
            link6_to_palm_translation,
            link6_to_palm_rotation,
        )
        joint_goal, solved = lula_solver.compute_inverse_kinematics(
            frame_name=EE_FRAME_NAME,
            target_position=np.asarray(link_position),
            target_orientation=np.asarray(link_orientation),
            warm_start=warm_start,
            position_tolerance=0.005,
            orientation_tolerance=np.deg2rad(5.0),
        )
        checked += 1
        print(f"   Plan IK      {state_name:8s} {'OK' if solved else 'FAILED'} {vec(target_tcp)}")
        if not solved:
            print(
                f"   전체 경로 사전 검사 실패: {state_name}. "
                "로봇을 움직이기 전에 안전 정지합니다."
            )
            return False
        warm_start = np.asarray(joint_goal, dtype=float)

    print(f"   Plan IK      전체 경로 {checked}개 자세 통과")
    return True


def compute_live_prim_center(stage, prim_path):
    """현재 물리 프레임에서 Prim의 월드 Bounding Box 중심을 다시 계산한다."""
    cache = UsdGeom.BBoxCache(
        Usd.TimeCode.Default(),
        [UsdGeom.Tokens.default_, UsdGeom.Tokens.render, UsdGeom.Tokens.proxy],
        useExtentsHint=True,
    )
    box = cache.ComputeWorldBound(require_prim(stage, prim_path)).ComputeAlignedBox()
    return np.array(box.GetMidpoint(), dtype=float)


def hold_world_for_inspection(world, reason):
    """오류 상태를 화면에서 확인할 수 있도록 Timeline을 멈추고 창을 유지한다."""
    print(f"   [SAFETY STOP] {reason}")
    world.pause()
    if args.headless:
        return
    print("   Stop은 초기 자세로 복귀하므로 누르지 말고 Pause 상태에서 확인하세요.")
    print("   Isaac Sim 창을 닫으면 프로그램이 종료됩니다.")
    while simulation_app.is_running():
        world.step(render=True)


def wait_for_play_after_stop(world):
    """Stop 뒤 사용자가 Play를 누를 때까지 로봇 handle에 접근하지 않는다."""
    print("   [RESTART] Stop을 감지했습니다. 다시 Play를 누르면 처음부터 재실행합니다.")
    while simulation_app.is_running():
        world.step(render=not args.headless)
        if world.is_playing():
            return True
    return False


def run_harvest_cycle(
    world,
    robot,
    stage,
    apple_center,
    conveyor_start,
    conveyor_outside,
    conveyor_top_z,
    conveyor_direction,
    link6_to_palm_translation,
    link6_to_palm_rotation,
):
    """초기 자세에서 한 번의 사과 수확을 수행한다.

    반환값이 ``restart``이면 GUI에서 Stop 후 Play가 입력된 것이다. 호출자는
    반드시 ``world.reset()``으로 PhysX handle을 다시 만든 뒤 이 함수를 새로
    호출해야 한다.
    """
    ik_solver, lula_solver = create_ik_solver(robot, stage)

    robot_position, _robot_orientation = get_prim_world_pose(stage, ROBOT_BASE_PATH)
    approach_rotation, approach_direction = make_approach_rotation(
        robot_position,
        apple_center,
    )
    current_tcp, _current_palm_rotation = current_tcp_pose(robot)
    pregrasp_tcp = apple_center - approach_direction * PREGRASP_DISTANCE_M

    gripper_indices = [robot.get_dof_index(name) for name in GRIPPER_JOINTS]
    apply_gripper_target(robot, gripper_indices, 0.0)

    print(f"   Start TCP    {vec(current_tcp)}")
    print(f"   Pregrasp TCP {vec(pregrasp_tcp)}")
    print(f"   Approach dir {vec(approach_direction)}")
    print("\n   시뮬레이션을 자동 시작합니다.\n")

    world.play()
    step = 0

    # 로봇을 사과 쪽으로 움직이기 전에 전체 경로를 검사한다. 사전 검사
    # 때문에 pregrasp에서 갑자기 멈추는 것으로 보이던 기존 순서를 없앤다.
    planned_fsm = AppleHarvestFSM(
        current_tcp=pregrasp_tcp,
        current_palm_rotation=approach_rotation,
        apple_center=apple_center,
        approach_rotation=approach_rotation,
        approach_direction=approach_direction,
        conveyor_start=conveyor_start,
        conveyor_outside=conveyor_outside,
        conveyor_top_z=conveyor_top_z,
        conveyor_direction=conveyor_direction,
        start_at_pregrasp=True,
    )
    initial_arm_positions = np.asarray(
        ik_solver.get_joints_subset().get_joint_positions(),
        dtype=float,
    )
    if not validate_planned_ik(
        planned_fsm,
        lula_solver,
        initial_arm_positions,
        pregrasp_tcp,
        approach_rotation,
        link6_to_palm_translation,
        link6_to_palm_rotation,
    ):
        hold_world_for_inspection(
            world,
            "전체 수확·운반 경로가 작업반경 밖이어서 로봇을 움직이지 않습니다.",
        )
        return "finished"

    transit_steps, transit_complete = move_arm_to_pregrasp(
        world=world,
        robot=robot,
        ik_solver=ik_solver,
        gripper_indices=gripper_indices,
        pregrasp_tcp=pregrasp_tcp,
        approach_rotation=approach_rotation,
        link6_to_palm_translation=link6_to_palm_translation,
        link6_to_palm_rotation=link6_to_palm_rotation,
        max_physics_steps=args.max_steps,
    )
    step += transit_steps

    if not transit_complete:
        if world.is_stopped():
            return "stopped"
        if args.max_steps > 0 and step >= args.max_steps:
            print(f"   --max-steps {args.max_steps} 도달 (TRANSIT 중)")
            return "finished"
        if not simulation_app.is_running():
            return "finished"
        raise RuntimeError("pregrasp 관절공간 이동을 완료하지 못했습니다.")

    # 실제 도달 pose에서 FSM을 시작해 Drive 추종 오차가 다음 단계에서
    # 불연속적인 목표 점프로 이어지지 않게 한다.
    current_tcp, current_palm_rotation = current_tcp_pose(robot)
    fsm = AppleHarvestFSM(
        current_tcp=current_tcp,
        current_palm_rotation=current_palm_rotation,
        apple_center=apple_center,
        approach_rotation=approach_rotation,
        approach_direction=approach_direction,
        conveyor_start=conveyor_start,
        conveyor_outside=conveyor_outside,
        conveyor_top_z=conveyor_top_z,
        conveyor_direction=conveyor_direction,
        start_at_pregrasp=True,
    )

    consecutive_ik_failures = 0
    completion_reported = False
    apple_grasp_verified = False
    safety_stop_reason = None
    stop_detected = False

    while simulation_app.is_running():
        world.step(render=not args.headless)

        # Stop은 Pause와 달리 PhysX handle을 파기한다. Stop 상태를 한 번이라도
        # 보았다면 이후 Play는 기존 객체의 계속 실행이 아니라 전체 재시작이다.
        if world.is_stopped():
            if not stop_detected:
                print("   [RESTART] Timeline Stop 감지: 로봇 handle 접근을 중지합니다.")
                print("   다시 Play를 누르면 초기 자세에서 수확을 재실행합니다.")
                stop_detected = True
            continue
        if stop_detected:
            if world.is_playing():
                return "restart"
            continue

        # 충돌이나 추종 실패가 감지되면 마지막 Drive 목표를 그대로 유지하고
        # Stage를 닫지 않는다. Stop 후 Play를 선택하면 새 사이클로 복구한다.
        if safety_stop_reason is not None:
            if world.is_playing():
                world.pause()
            if not completion_reported:
                print(f"   [SAFETY STOP] {safety_stop_reason}")
                print("   Timeline을 Pause했습니다. 로봇과 컨베이어 배치를 확인하세요.")
                print("   다시 실행하려면 Stop을 누른 뒤 Play를 누르세요.")
                completion_reported = True
            if args.headless:
                return "finished"
            continue

        if not world.is_playing():
            continue

        # 완료 자세에서는 로봇 handle을 건드리지 않는다. Stop 후 Play를 누르면
        # 위의 stop_detected 분기가 새 Articulation으로 재실행을 요청한다.
        if fsm.done:
            if not completion_reported:
                print("   완료 자세를 유지합니다.")
                print("   다시 보려면 Stop을 누른 뒤 Play를 누르세요.")
                completion_reported = True
            if args.headless:
                return "finished"
            continue

        target_tcp, target_palm_rotation, close_ratio = fsm.sample()
        link_position, link_orientation = tcp_target_to_link6(
            target_tcp,
            target_palm_rotation,
            link6_to_palm_translation,
            link6_to_palm_rotation,
        )

        arm_action, solved = ik_solver.compute_inverse_kinematics(
            target_position=link_position,
            target_orientation=link_orientation,
            position_tolerance=0.003,
            orientation_tolerance=np.deg2rad(3.0),
        )

        if solved:
            robot.apply_action(arm_action)
            consecutive_ik_failures = 0
            actual_tcp, actual_rotation = current_tcp_pose(robot)
            advance_status = fsm.advance(actual_tcp, actual_rotation)
            if advance_status == "timeout":
                state_name = fsm.NAMES[min(fsm.state, len(fsm.NAMES) - 1)]
                safety_stop_reason = (
                    f"{state_name} 목표를 실제 TCP가 따라가지 못했습니다. "
                    "충돌 또는 Drive 추종 실패 가능성이 있습니다."
                )

            # RETREAT 완료 시 사과가 TCP 가까이에 실제로 따라왔는지 확인한다.
            next_state = fsm.NAMES[min(fsm.state, len(fsm.NAMES) - 1)]
            if (
                advance_status == "advanced"
                and next_state == "CLEAR_UP"
                and not apple_grasp_verified
            ):
                live_apple_center = compute_live_prim_center(stage, APPLE_PATH)
                apple_distance = float(np.linalg.norm(live_apple_center - actual_tcp))
                print(
                    f"   Apple grasp  center {vec(live_apple_center)}, "
                    f"TCP distance {apple_distance:.4f} m"
                )
                if apple_distance > APPLE_GRASP_MAX_DISTANCE_M:
                    safety_stop_reason = (
                        "사과가 그리퍼를 따라오지 않았습니다. "
                        f"TCP와 사과 중심 거리 {apple_distance:.3f} m"
                    )
                else:
                    apple_grasp_verified = True
        else:
            consecutive_ik_failures += 1
            if consecutive_ik_failures == 1 or consecutive_ik_failures % 60 == 0:
                print(
                    f"   IK FAILED x{consecutive_ik_failures}: "
                    f"TCP {vec(target_tcp)}"
                )
            if consecutive_ik_failures >= MAX_CONSECUTIVE_IK_FAILURES:
                state_name = fsm.NAMES[min(fsm.state, len(fsm.NAMES) - 1)]
                safety_stop_reason = (
                    f"{state_name} 구간의 IK가 "
                    f"{MAX_CONSECUTIVE_IK_FAILURES}회 연속 실패했습니다. "
                    "컨베이어가 작업반경 밖인지 확인하세요."
                )

        if safety_stop_reason is None:
            apply_gripper_target(robot, gripper_indices, close_ratio)

        if step % 60 == 0:
            actual_tcp, _actual_rotation = current_tcp_pose(robot)
            state_name = fsm.NAMES[min(fsm.state, len(fsm.NAMES) - 1)]
            print(
                f"   {state_name:8s} target {vec(target_tcp)} "
                f"actual {vec(actual_tcp)} grip {close_ratio:.2f}"
            )

        step += 1
        if args.max_steps > 0 and step >= args.max_steps:
            print(f"   --max-steps {args.max_steps} 도달")
            return "finished"

    return "finished"


# ══════════════════════════════════════════════════════════════
# 메인
# ══════════════════════════════════════════════════════════════
def main():
    print("\n" + "═" * 72)
    print(" M0617 + Robotiq 3F Apple Harvest")
    print("═" * 72)

    stage = open_project_stage()
    configure_breakable_joint(stage)
    configure_contact_colliders(stage)
    configure_joint_drives(stage)
    apple_center, apple_size = compute_apple_center(stage)
    link6_to_palm_translation, link6_to_palm_rotation = compute_link6_to_palm(stage)
    robot_stage_position, _robot_stage_orientation = get_prim_world_pose(
        stage, ROBOT_BASE_PATH
    )
    conveyor_start, conveyor_outside, conveyor_top_z, conveyor_direction = (
        compute_conveyor_start(stage, robot_stage_position, apple_size)
    )

    world = World(
        stage_units_in_meters=1.0,
        physics_prim_path="/physicsScene",
        physics_dt=1.0 / 60.0,
        rendering_dt=1.0 / 60.0,
    )
    robot = create_robot(world)

    try:
        cycle = 1
        while simulation_app.is_running():
            if cycle > 1:
                print("\n" + "─" * 72)
                print(f" 수확 사이클 {cycle}: 물리·Articulation·IK 재초기화")
                print("─" * 72)
                # 같은 SingleManipulator를 Scene에 중복 등록하지 않고, Stop으로
                # 해제된 PhysX view와 모든 articulation handle만 다시 만든다.
                world.reset()

            result = run_harvest_cycle(
                world=world,
                robot=robot,
                stage=stage,
                apple_center=apple_center,
                conveyor_start=conveyor_start,
                conveyor_outside=conveyor_outside,
                conveyor_top_z=conveyor_top_z,
                conveyor_direction=conveyor_direction,
                link6_to_palm_translation=link6_to_palm_translation,
                link6_to_palm_rotation=link6_to_palm_rotation,
            )

            if result == "stopped":
                if not wait_for_play_after_stop(world):
                    break
                result = "restart"

            if result != "restart":
                break

            # 사용자가 누른 Play는 해제된 이전 handle을 가리킬 수 있다. 다음
            # 반복에서 world.reset()한 뒤 solver/FSM을 새로 만들어 실행한다.
            cycle += 1

    except KeyboardInterrupt:
        print("\n   사용자가 실행을 중단했습니다.")
    finally:
        world.stop()
        simulation_app.close()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # 초기화 단계 오류도 창을 즉시 닫지 않는다. Traceback을 출력한 뒤
        # 사용자가 Stage와 로그를 확인할 수 있도록 GUI 업데이트만 유지한다.
        traceback.print_exc()
        if not args.headless and simulation_app.is_running():
            print("   [SETUP ERROR] 오류 확인을 위해 Isaac Sim 창을 유지합니다.")
            print("   창을 닫으면 프로그램이 종료됩니다.")
            while simulation_app.is_running():
                simulation_app.update()
        simulation_app.close()
