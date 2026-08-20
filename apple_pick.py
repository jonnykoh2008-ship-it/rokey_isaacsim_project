"""
M0617 + Robotiq 3F 그리퍼 사과 수확 동작

실행:
    /home/rokey/isaacsim/python.sh apple_pick.py

헤드리스 점검:
    /home/rokey/isaacsim/python.sh apple_pick.py --headless --max-steps 300

동작 순서:
    현재 자세 -> 사과 앞 접근 -> 사과 중심 진입 -> 3F 그리퍼 닫기
    -> 접근축 기준 45도 회전(1초) -> 로봇 방향으로 당기기 -> 후퇴

중요:
    * 이 코드는 기존 USD/URDF를 저장하거나 수정하지 않는다.
    * FixedJoint의 파손 한계 15 N / 0.6 N·m는 실행 중인 Stage에만 적용한다.
    * 15 N은 당기는 명령값이 아니라 Joint가 끊어지는 반력 한계다.
"""

import argparse
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

ROBOT_PRIM_PATH = "/World/m0617"
LINK6_PATH = "/World/m0617/link_6"
GRIPPER_ROOT_PATH = "/World/m0617/robotiq_3f_gripper_articulated"
PALM_PATH = "/World/m0617/robotiq_3f_gripper_articulated/palm"
APPLE_PATH = "/World/Xform/applebody/apple1"
FIXED_JOINT_PATH = "/World/Xform/FixedJoint"

EE_FRAME_NAME = "link_6"
ARM_JOINTS = [f"joint_{index}" for index in range(1, 7)]


# ══════════════════════════════════════════════════════════════
# 사과 분리와 이동 조건
# ══════════════════════════════════════════════════════════════
BREAK_FORCE_N = 15.0
BREAK_TORQUE_NM = 0.6

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


# ══════════════════════════════════════════════════════════════
# Stage 검사와 물리 설정
# ══════════════════════════════════════════════════════════════
def require_prim(stage, prim_path):
    prim = stage.GetPrimAtPath(prim_path)
    if not prim.IsValid():
        raise RuntimeError(f"필수 Prim을 찾을 수 없습니다: {prim_path}")
    return prim


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
        ROBOT_PRIM_PATH,
        LINK6_PATH,
        PALM_PATH,
        APPLE_PATH,
        FIXED_JOINT_PATH,
    ):
        require_prim(stage, prim_path)

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
            drive.GetStiffnessAttr().Set(1.0e8)
            drive.GetDampingAttr().Set(1.0e4)
            drive.GetMaxForceAttr().Set(1.0e8)
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
    return center


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


# ══════════════════════════════════════════════════════════════
# 수확 상태 기계
# ══════════════════════════════════════════════════════════════
class AppleHarvestFSM:
    """접근부터 비틀기·당기기·후퇴까지 목표 pose를 연속으로 만든다."""

    NAMES = ["APPROACH", "ENTER", "GRASP", "TWIST", "PULL", "RETREAT", "DONE"]

    def __init__(self, current_tcp, current_palm_rotation, apple_center, approach_rotation, approach_direction):
        self.apple_center = np.asarray(apple_center, dtype=float)
        self.approach_rotation = np.asarray(approach_rotation, dtype=float)
        self.approach_direction = np.asarray(approach_direction, dtype=float)
        self.twisted_rotation = approach_rotation @ rotation_about_y(np.deg2rad(TWIST_DEG))

        pregrasp = apple_center - approach_direction * PREGRASP_DISTANCE_M
        pull = apple_center - approach_direction * PULL_DISTANCE_M
        retreat = (
            apple_center
            - approach_direction * RETREAT_DISTANCE_M
            + np.array([0.0, 0.0, RETREAT_HEIGHT_M])
        )

        approach_steps = int(
            np.clip(
                np.linalg.norm(pregrasp - current_tcp) / TCP_STEP_M,
                MIN_MOVE_STEPS,
                MAX_MOVE_STEPS,
            )
        )

        self.specs = [
            (pregrasp, approach_rotation, approach_steps, 0.0, 0.0),
            (apple_center, approach_rotation, 100, 0.0, 0.0),
            (apple_center, approach_rotation, 120, 0.0, 1.0),
            (apple_center, self.twisted_rotation, TWIST_STEPS, 1.0, 1.0),
            (pull, self.twisted_rotation, 120, 1.0, 1.0),
            (retreat, self.twisted_rotation, 180, 1.0, 1.0),
        ]

        self.state = 0
        self.frame = 0
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

    def advance(self):
        """IK가 성공한 물리 스텝만 진행한다."""
        if self.done:
            return

        self.frame += 1
        _goal_position, goal_rotation, steps, _grip0, _grip1 = self.specs[self.state]
        if self.frame < steps:
            return

        goal_position = self.specs[self.state][0]
        self.start_position = np.asarray(goal_position, dtype=float)
        self.start_quat = rot_matrix_to_quat(goal_rotation)
        self.state += 1
        self.frame = 0
        self._print_state()


# ══════════════════════════════════════════════════════════════
# 로봇과 IK 초기화
# ══════════════════════════════════════════════════════════════
def create_robot(world):
    """기존 Stage의 M0617 전체 Articulation을 Python 객체로 등록한다."""
    robot = world.scene.add(
        SingleManipulator(
            prim_path=ROBOT_PRIM_PATH,
            end_effector_prim_path=PALM_PATH,
            name="m0617_3f_robot",
            gripper=None,
        )
    )
    # world.reset()이 Scene에 등록된 Articulation과 end-effector를 함께
    # 초기화한다. 여기서 robot.initialize()를 다시 호출하면 PhysX view가
    # 중복 생성되어 non-root link 관련 경고가 발생할 수 있다.
    world.reset()

    missing = [name for name in ARM_JOINTS + GRIPPER_JOINTS if name not in robot.dof_names]
    if missing:
        raise RuntimeError(f"Articulation에서 관절을 찾을 수 없습니다: {missing}")

    print(f"   Articulation {robot.num_dof} DOF")
    for index, name in enumerate(robot.dof_names):
        group = "arm" if name in ARM_JOINTS else "3f"
        print(f"      [{index:2d}] {name:28s} {group}")
    return robot


def create_ik_solver(robot):
    """M0617 6축만 제어하는 Lula IK를 만든다."""
    lula = LulaKinematicsSolver(
        robot_description_path=str(DESCRIPTION_PATH),
        urdf_path=str(URDF_PATH),
    )
    base_position, base_orientation = robot.get_world_pose()
    lula.set_robot_base_pose(
        robot_position=np.asarray(base_position),
        robot_orientation=np.asarray(base_orientation),
    )
    print(f"   Robot base   {vec(base_position)}")
    print(f"   Lula joints  {', '.join(lula.get_joint_names())}")
    return ArticulationKinematicsSolver(
        robot_articulation=robot,
        kinematics_solver=lula,
        end_effector_frame_name=EE_FRAME_NAME,
    )


def apply_gripper_target(robot, gripper_indices, close_ratio):
    """0.0=open, 1.0=closed 비율로 11개 그리퍼 관절을 명령한다."""
    targets = GRIPPER_OPEN + close_ratio * (GRIPPER_CLOSED - GRIPPER_OPEN)
    robot.apply_action(
        ArticulationAction(
            joint_positions=targets,
            joint_indices=np.asarray(gripper_indices, dtype=np.int32),
        )
    )


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
    apple_center = compute_apple_center(stage)
    link6_to_palm_translation, link6_to_palm_rotation = compute_link6_to_palm(stage)

    world = World(
        stage_units_in_meters=1.0,
        physics_prim_path="/physicsScene",
        physics_dt=1.0 / 60.0,
        rendering_dt=1.0 / 60.0,
    )
    robot = create_robot(world)
    ik_solver = create_ik_solver(robot)

    robot_position, _robot_orientation = robot.get_world_pose()
    approach_rotation, approach_direction = make_approach_rotation(robot_position, apple_center)
    current_tcp, current_palm_rotation = current_tcp_pose(robot)
    fsm = AppleHarvestFSM(
        current_tcp=current_tcp,
        current_palm_rotation=current_palm_rotation,
        apple_center=apple_center,
        approach_rotation=approach_rotation,
        approach_direction=approach_direction,
    )

    gripper_indices = [robot.get_dof_index(name) for name in GRIPPER_JOINTS]
    apply_gripper_target(robot, gripper_indices, 0.0)

    print(f"   Start TCP    {vec(current_tcp)}")
    print(f"   Approach dir {vec(approach_direction)}")
    print("\n   시뮬레이션을 자동 시작합니다.\n")

    world.play()
    step = 0
    consecutive_ik_failures = 0

    try:
        while simulation_app.is_running():
            world.step(render=not args.headless)
            if not world.is_playing():
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
                fsm.advance()
                consecutive_ik_failures = 0
            else:
                consecutive_ik_failures += 1
                if consecutive_ik_failures == 1 or consecutive_ik_failures % 60 == 0:
                    print(
                        f"   IK FAILED x{consecutive_ik_failures}: "
                        f"TCP {vec(target_tcp)}"
                    )

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
                break
            if args.headless and fsm.done:
                break

    except KeyboardInterrupt:
        print("\n   사용자가 실행을 중단했습니다.")
    finally:
        world.stop()
        simulation_app.close()


if __name__ == "__main__":
    main()
