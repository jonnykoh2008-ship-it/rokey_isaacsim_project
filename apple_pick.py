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
    * FixedJoint의 파손 한계는 실행 중인 Stage에만 적용한다.
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
parser.add_argument(
    "--break-test",
    choices=("both", "force", "torque"),
    default="both",
    help=(
        "FixedJoint 파손 진단: both=15N/지정 torque, "
        "force=15N/최대 torque, torque=최대 force/지정 torque"
    ),
)
parser.add_argument(
    "--break-torque-nm",
    type=float,
    default=1.0,
    help="torque/both 진단 모드의 break torque (기본값: 1.0 N·m)",
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

import omni.physx
import omni.usd
from omni.physx.bindings._physx import SimulationEvent
from pxr import Gf, PhysicsSchemaTools, PhysxSchema, Usd, UsdGeom, UsdPhysics

from isaacsim.core.api import World
from isaacsim.core.api.objects import VisualCuboid, VisualSphere
from isaacsim.core.utils.rotations import quat_to_rot_matrix, rot_matrix_to_quat
from isaacsim.core.utils.stage import is_stage_loading
from isaacsim.core.utils.types import ArticulationAction
from isaacsim.robot.manipulators.manipulators import SingleManipulator
from isaacsim.robot_motion.motion_generation import (
    ArticulationKinematicsSolver,
    ArticulationMotionPolicy,
    LulaKinematicsSolver,
    RmpFlow,
)


# ══════════════════════════════════════════════════════════════
# 파일과 Stage Prim 경로
# ══════════════════════════════════════════════════════════════
PROJECT_DIR = Path(__file__).resolve().parent
STAGE_PATH = PROJECT_DIR / "m0617_3fgripper08201638.usd"
DESCRIPTION_PATH = PROJECT_DIR / "m0617_robot_description.yaml"
RMPFLOW_CONFIG_PATH = PROJECT_DIR / "m0617_rmpflow_config.yaml"
URDF_PATH = (
    PROJECT_DIR
    / "m0617_gripper"
    / "dsr_description2"
    / "urdf"
    / "m0617.urdf"
)

ARTICULATION_PRIM_PATH = "/World/Xform_01/m0617_rail"
ARTICULATION_ROOT_JOINT_PATH = "/World/Xform_01/m0617_rail/root_joint"
RAIL_JOINT_PATH = "/World/Xform_01/m0617_rail/joints/rail_joint"
ROBOT_MOUNT_JOINT_PATH = "/World/FixedJoint"
ROBOT_PRIM_PATH = "/World/Xform_01/m0617"
ROBOT_BASE_PATH = "/World/Xform_01/m0617/base_link"
LINK6_PATH = "/World/Xform_01/m0617/link_6"
GRIPPER_ROOT_PATH = "/World/Xform_01/m0617/robotiq_3f_gripper_articulated"
PALM_PATH = "/World/Xform_01/m0617/robotiq_3f_gripper_articulated/palm"
APPLE_PATH = "/World/Xform/apple_branchbody/applebody/apple1"
FIXED_JOINT_PATH = "/World/Xform/FixedJoint"
BRANCH_BODY_PATH = "/World/Xform/apple_branchbody/branchbody"
TREE_ROOT_PATH = "/World/Xform/tree"
PLANNING_OBSTACLE_ROOT_PATH = "/World/RuntimeHarvestPlanningObstacles"
CONVEYOR_PATH = "/World/ConveyorBelt_A08_PR_NVD_01"
RUNTIME_CONVEYOR_COLLIDER_PATH = "/World/RuntimeConveyorBeltSurface"
FIXED_CAMERA_ROOT_PATHS = ["/World/base_rsd455", "/conv_rsd455"]

# compute_conveyor_start()가 실제 Stage 경계에서 계산한 값만 보관한다.
# 컨베이어 안전거리 임계값은 문서에서 TBD이므로 여기서 임의로 더하지 않는다.
_CONVEYOR_PLANNING_GEOMETRY = None

EE_FRAME_NAME = "link_6"
_LINK6_TO_PALM_TRANSLATION = None
_LINK6_TO_PALM_ROTATION = None
RAIL_JOINT = "rail_joint"
ARM_JOINTS = [f"joint_{index}" for index in range(1, 7)]


# ══════════════════════════════════════════════════════════════
# 사과 분리와 이동 조건
# ══════════════════════════════════════════════════════════════
BREAK_FORCE_N = 15.0
BREAK_TORQUE_NM = 1.0

# palm collision mesh 앞면(+Y 50.8 mm)과 명목 사과 반지름(40 mm)을 합친 포위
# 파지 중심이다. 접촉 여유는 현재 0 mm이므로 실효 offset은 90.8 mm이며,
# docs/features/harvesting.md의 명목 80 mm 사과 중심 목표(+Y 90.8 mm)와
# 일치한다. docs/architecture/tf_frames.md는 접촉 여유 2.2 mm를 포함한
# 93 mm를 명시하므로 두 문서 값이 서로 다르다. 여유를 되살리려면
# PALM_CONTACT_CLEARANCE_M만 조정한다. 기존 125 mm는 사과와 palm 사이에
# 약 34 mm 틈을 남겨 손가락 끝만 접촉하므로 사용하지 않는다.
PALM_COLLISION_FACE_Y_M = 0.0508
NOMINAL_APPLE_RADIUS_M = 0.0400
PALM_CONTACT_CLEARANCE_M = 0.0
PALM_TO_TCP = np.array(
    [
        0.0,
        PALM_COLLISION_FACE_Y_M
        + NOMINAL_APPLE_RADIUS_M
        + PALM_CONTACT_CLEARANCE_M,
        0.0,
    ],
    dtype=float,
)

PREGRASP_DISTANCE_M = 0.15
ENTER_SLOW_DISTANCE_M = 0.03
ENTER_FAST_STEPS = 360
ENTER_SLOW_STEPS = 360
ENTRY_PRESHAPE_SAMPLE_STEPS = 30
ENTRY_PRESHAPE_MAX_SETTLE_STEPS = 120
# entry pre-shape에서 손가락 collider가 사과를 지나칠 때 요구할 최소 여유이다.
# 그리퍼를 최대로 벌린 상태의 기계적 최대 여유가 명목 80 mm 사과 기준 약
# 0.0137 m이므로 이 값은 그보다 작아야 한다. 그렇지 않으면 정상 사과도
# 전부 거부된다. 0.010 m는 지름 약 87 mm까지 허용하고 그보다 큰 사과는
# 진입 전에 APPROACH_UNREACHABLE로 중단시키는 임시값이다.
ENTRY_SWEEP_MIN_CLEARANCE_M = 0.010
APPLE_OBSTACLE_RELEASE_DISTANCE_M = 0.30
PULL_DISTANCE_M = 0.10
RETREAT_DISTANCE_M = 0.25
RETREAT_HEIGHT_M = 0.15
TWIST_DEG = 45.0
TWIST_STEPS = 60  # Stage가 60 Hz일 때 약 1초
# Action 단계별 3초 simulation-time 제한 안에서 팔 정착과 폐합을
# 마친다. stem break 한계 자체는 변경하지 않는다.
GRASP_SETTLE_STEPS = 30
GRASP_STEPS = 120

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
# 손가락이 상판에 닿기 전에 사과를 놓는다. 사과는 약 3 cm만 자유낙하하므로
# 컨베이어와 직접 충돌하면서 억지로 밀어 넣는 것보다 충격이 작다.
RELEASE_CLEARANCE_M = 0.030
PLACE_VERTICAL_LIFT_M = 0.060
PLACE_TRANSIT_STEP_M = 0.0015
PLACE_DESCENT_STEP_M = 0.0005
PLACE_ROTATE_STEPS = 180
RELEASE_STEPS = 120
PLACE_LIFT_STEPS = 150
MAX_CONSECUTIVE_IK_FAILURES = 180
TARGET_POSITION_TOLERANCE_M = 0.025
TARGET_ORIENTATION_TOLERANCE_DEG = 6.0
# 마지막 pre-grasp waypoint는 여기서 swept clearance를 측정하고 곧바로
# 사과 사이로 진입하므로 일반 transit 허용오차를 쓸 수 없다. 25 mm 도착
# 오차는 ENTER 중 횡방향으로 되밀어야 하는 거리가 되어 진입 여유(명목
# 사과 기준 약 13.8 mm)를 통째로 잡아먹는다. RMPflow가 실제로 낼 수 있는
# 정밀도는 미검증이므로 [TRANSIT] 실측값을 보고 조정할 임시값이다.
PREGRASP_POSITION_TOLERANCE_M = 0.005
PREGRASP_ORIENTATION_TOLERANCE_DEG = 2.0
MAX_TARGET_SETTLE_STEPS = 180
APPLE_GRASP_MAX_DISTANCE_M = 0.14

# RMPflow planning proxy와 재계획의 초기값이다. 문서의 최소 안전거리를
# obstacle 반경/크기에 더하며, 실제 시뮬레이션 충돌 시험 후 튜닝한다.
THICK_BRANCH_CLEARANCE_M = 0.050
SMALL_BRANCH_CLEARANCE_M = 0.020
BRANCH_PROXY_VOXEL_M = 0.060
# RMPflow local-minimum을 피하기 위한 시뮬레이션 튜닝 임시값이다. 실제
# 안전거리는 각 proxy 반경에 별도로 포함되므로 아래 값은 후보의 범위와 수만
# 제한한다.
PLANNING_CORRIDOR_RADIUS_M = 0.25
START_PROXY_EXCLUSION_RADIUS_M = 0.18
MAX_BRANCH_PROXIES = 48
TARGET_APPLE_OBSTACLE_RADIUS_M = 0.060
RMPFLOW_MAXIMUM_SUBSTEP_S = 1.0 / 300.0
RMPFLOW_SEGMENT_STEPS = 360
RMPFLOW_REPLAN_OFFSET_M = 0.20
TREE_OUTSIDE_WAYPOINT_OFFSET_M = 0.45
RMPFLOW_STALL_STEPS = 120
RMPFLOW_STALL_POSITION_DELTA_M = 0.005
RMPFLOW_STALL_ROTATION_DELTA_DEG = 2.0

# 충돌 시 1e8 수준의 강한 Drive가 컨베이어를 억지로 뚫지 않도록 제한한다.
# M0617이 느린 보간 목표를 추종할 수 있는 범위에서 보수적으로 낮춘 값이다.
ARM_DRIVE_STIFFNESS = 1.0e6
ARM_DRIVE_DAMPING = 1.0e4
ARM_DRIVE_MAX_FORCE = 2.0e3
GRIPPER_DRIVE_STIFFNESS = 50.0
GRIPPER_DRIVE_DAMPING = 5.0
# 11개 손가락 관절의 동시 접촉 토크가 stem의 1 N·m 한계에 집중되지 않도록
# GRASP는 저토크로 접촉하고, TWIST/PULL과 운반 중에는 사과가 미끄러지지
# 않도록 유지 토크를 높인다. 실제 파지 시험 후 재조정할 임시값이다.
GRIPPER_GRASP_MAX_FORCE = 0.08
GRIPPER_HOLD_MAX_FORCE = 0.50
GRIPPER_DRIVE_MAX_FORCE = GRIPPER_GRASP_MAX_FORCE
# entry pre-shape는 사과에 닿기 전 자세라 stem의 1 N·m 제한과 무관하다.
# GRASP용 저토크로는 팔이 가속하는 동안 손가락이 명령 자세를 유지하지 못해
# 정적으로 측정한 swept clearance와 실제 진입 자세가 달라질 수 있다.
GRIPPER_ENTRY_MAX_FORCE = GRIPPER_HOLD_MAX_FORCE
# 진입 중 실시간으로 다시 잰 swept clearance가 이 값 아래로 내려가면
# 중단한다. 검사 간격 동안 진행하는 거리보다 커야 접촉 전에 멈출 수 있다.
ENTRY_LIVE_MIN_CLEARANCE_M = 0.004
ENTRY_LIVE_CHECK_INTERVAL_STEPS = 10

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

# 사과 진입/해제 자세는 두 측면 손가락의 palm joint를 URDF 허용 범위
# 바깥쪽 끝까지 벌린다. 세 distal joint는 음의 limit 근처로 접어 전방으로
# 길게 뻗은 손가락 끝을 사과 통로 바깥쪽으로 빼는 entry pre-shape이다.
# 단순 all-zero 자세는 영상상 palm보다 약 0.11 m 앞에서 선접촉했다.
GRIPPER_OPEN = np.array(
    [
        0.25,
        0.0,
        0.0,
        -1.20,
        -0.25,
        0.0,
        0.0,
        -1.20,
        0.0,
        0.0,
        -1.20,
    ],
    dtype=float,
)

# URDF(robotiq_3f_isaac.urdf)의 손가락 관절 한계이다. 진입 여유를 넓히는
# 방향은 proximal/medial을 펴고(0) distal을 최대로 접는(음의 한계) 쪽뿐이다.
FINGER_JOINT_1_LOWER_RAD = 0.0
FINGER_JOINT_2_LOWER_RAD = 0.0
FINGER_JOINT_3_LOWER_RAD = -1.2217304764
# Drive가 한계에 정확히 붙으면 solver가 진동할 수 있어 여유를 둔다.
FINGER_LIMIT_MARGIN_RAD = 0.005
ENTRY_DISTAL_MAX_RAD = FINGER_JOINT_3_LOWER_RAD + FINGER_LIMIT_MARGIN_RAD


def _entry_preshape(distal_rad):
    """두 측면 palm joint를 최대로 벌리고 세 distal을 지정 각도로 접는다."""
    return np.array(
        [
            0.25, FINGER_JOINT_1_LOWER_RAD, FINGER_JOINT_2_LOWER_RAD, distal_rad,
            -0.25, FINGER_JOINT_1_LOWER_RAD, FINGER_JOINT_2_LOWER_RAD, distal_rad,
            FINGER_JOINT_1_LOWER_RAD, FINGER_JOINT_2_LOWER_RAD, distal_rad,
        ],
        dtype=float,
    )


# pre-grasp에서 실제 collider swept clearance를 측정할 후보이다.
# 이전 버전은 finger_middle_joint_1을 0.00~0.60으로 키우며 탐색했지만 URDF
# 하한이 0이므로 값을 키우는 방향은 손가락을 사과 통로 안쪽으로 감을 뿐이다.
# 실측에서도 0.00/0.10/0.35/0.60의 여유가 각각 13.8/11.9/5.1/-8.1 mm로
# 단조 감소해 항상 0.00이 선택됐다. 남은 자유도는 distal 굽힘뿐이므로
# 기본값과 URDF 한계 두 가지만 비교한다.
GRIPPER_ENTRY_CANDIDATES = [
    ("distal_-1.20", GRIPPER_OPEN.copy()),
    (f"distal_{ENTRY_DISTAL_MAX_RAD:.4f}", _entry_preshape(ENTRY_DISTAL_MAX_RAD)),
]

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


def resolve_unique_named_prim_path(stage, prim_name):
    """재그룹된 asset에서 이름이 일치하는 유일한 Prim 경로를 찾는다."""
    matches = [
        str(prim.GetPath())
        for prim in stage.Traverse()
        if str(prim.GetName()) == prim_name
    ]
    if len(matches) != 1:
        raise RuntimeError(
            f"'{prim_name}' Prim이 유일하지 않습니다: "
            f"count={len(matches)}, paths={matches}"
        )
    return matches[0]


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
    expected0 = ["/World/Xform_01/m0617_rail/rail_robot_mount_link"]
    expected1 = [ROBOT_BASE_PATH]
    if body0 != expected0 or body1 != expected1:
        raise RuntimeError(
            "레일-M0617 FixedJoint 대상이 예상과 다릅니다: "
            f"Body0={body0}, Body1={body1}"
        )


def open_project_stage():
    """저장된 조립 USD를 열고 모든 참조가 로드될 때까지 기다린다."""
    global APPLE_PATH, BRANCH_BODY_PATH

    for path in (STAGE_PATH, DESCRIPTION_PATH, RMPFLOW_CONFIG_PATH, URDF_PATH):
        if not path.exists():
            raise FileNotFoundError(path)

    omni.usd.get_context().open_stage(str(STAGE_PATH))
    simulation_app.update()
    simulation_app.update()
    while is_stage_loading():
        simulation_app.update()

    stage = omni.usd.get_context().get_stage()
    APPLE_PATH = resolve_unique_named_prim_path(stage, "apple1")
    BRANCH_BODY_PATH = resolve_unique_named_prim_path(stage, "branchbody")
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
    print(f"   Apple prim   {APPLE_PATH}")
    print(f"   Branch prim  {BRANCH_BODY_PATH}")
    return stage


def configure_breakable_joint(stage):
    """USD에 저장된 사과-가지 FixedJoint를 검증하고 그대로 사용한다."""
    joint_prim = require_prim(stage, FIXED_JOINT_PATH)
    joint = UsdPhysics.Joint(joint_prim)

    body0 = [str(path) for path in joint.GetBody0Rel().GetTargets()]
    body1 = [str(path) for path in joint.GetBody1Rel().GetTargets()]
    apple_body_path = str(require_prim(stage, APPLE_PATH).GetParent().GetPath())
    expected0 = [BRANCH_BODY_PATH]
    expected1 = [apple_body_path]
    if body0 != expected0 or body1 != expected1:
        raise RuntimeError(
            "FixedJoint Body 대상이 예상과 다릅니다: "
            f"Body0={body0}, Body1={body1}"
        )

    break_force, break_torque = configured_break_limits()
    joint.GetBreakForceAttr().Set(break_force)
    joint.GetBreakTorqueAttr().Set(break_torque)
    joint.GetJointEnabledAttr().Set(True)
    joint.GetCollisionEnabledAttr().Set(False)

    # USD 단독 Play에서 검증된 원본 구성을 유지한다. branchbody는
    # kinematic rigid body이며, 이 body와 applebody 사이의 authored
    # anchor가 사과를 가지에 고정한다.
    branch_prim = require_prim(stage, BRANCH_BODY_PATH)
    if not branch_prim.HasAPI(UsdPhysics.RigidBodyAPI):
        raise RuntimeError(f"가지 RigidBodyAPI가 없습니다: {BRANCH_BODY_PATH}")
    branch_rigid_body = UsdPhysics.RigidBodyAPI(branch_prim)
    branch_rigid_body.GetRigidBodyEnabledAttr().Set(True)
    branch_rigid_body.GetKinematicEnabledAttr().Set(True)

    print(
        f"   Apple joint  authored {FIXED_JOINT_PATH}, "
        f"body0 {BRANCH_BODY_PATH}, body1 {apple_body_path}"
    )
    print(
        f"   Apple joint  break test {args.break_test}: "
        f"force {break_force:.3g} N, torque {break_torque:.3g} N·m"
    )


def configured_break_limits():
    """선택한 진단 모드에 따라 한쪽 파손 한계만 격리한다."""
    maximum = float(np.finfo(np.float32).max)
    break_torque = float(args.break_torque_nm)
    if not np.isfinite(break_torque) or break_torque <= 0.0:
        raise RuntimeError(
            f"--break-torque-nm은 0보다 큰 유한값이어야 합니다: {break_torque}"
        )
    if args.break_test == "force":
        return BREAK_FORCE_N, maximum
    if args.break_test == "torque":
        return maximum, break_torque
    return BREAK_FORCE_N, break_torque


class JointBreakMonitor:
    """사과 FixedJoint의 실제 PhysX 파손 시점과 FSM 상태를 기록한다."""

    def __init__(self, stage):
        self.stage = stage
        branch_prim = require_prim(stage, BRANCH_BODY_PATH)
        self.branch_imageable = UsdGeom.Imageable(branch_prim)
        if not self.branch_imageable:
            raise RuntimeError(
                f"가지 prim에 visibility를 적용할 수 없습니다: {BRANCH_BODY_PATH}"
            )
        self.broken = False
        self.break_state = None
        self.current_state = "SETUP"
        self._set_branch_visible(True)
        events = omni.physx.get_physx_interface().get_simulation_event_stream_v2()
        self._subscription = events.create_subscription_to_pop(self._on_event)

    def _set_branch_visible(self, visible):
        """런타임 세션 레이어에서 branchbody의 렌더링만 전환한다."""
        visibility = (
            UsdGeom.Tokens.inherited if visible else UsdGeom.Tokens.invisible
        )
        with Usd.EditContext(self.stage, self.stage.GetSessionLayer()):
            if not self.branch_imageable.CreateVisibilityAttr().Set(visibility):
                raise RuntimeError(
                    f"가지 visibility를 설정하지 못했습니다: {BRANCH_BODY_PATH}"
                )

    def set_state(self, state):
        self.current_state = state

    def reset(self):
        self.broken = False
        self.break_state = None
        self.current_state = "SETUP"
        self._set_branch_visible(True)

    def close(self):
        self._subscription = None

    def _on_event(self, event):
        if event.type != int(SimulationEvent.JOINT_BREAK):
            return
        encoded_path = event.payload.get("jointPath", None)
        if encoded_path is None:
            return
        joint_path = PhysicsSchemaTools.decodeSdfPath(
            encoded_path[0], encoded_path[1]
        )
        if str(joint_path) != FIXED_JOINT_PATH:
            return
        self.broken = True
        self.break_state = self.current_state
        self._set_branch_visible(False)
        break_force, break_torque = configured_break_limits()
        print(
            f"   [JOINT BREAK] {FIXED_JOINT_PATH} state={self.break_state}, "
            f"test={args.break_test}, "
            f"limit={break_force:.3g} N/{break_torque:.3g} N·m"
        )
        print(f"   [BRANCH HIDDEN] {BRANCH_BODY_PATH}")


class RobotTreeContactMonitor:
    """실제 로봇 collider와 나무·컨베이어 접촉을 매 physics step 감시한다."""

    def __init__(self, stage):
        self.detected = False
        self.state = "IDLE"
        self.robot_path = None
        self.tree_path = None
        articulation = require_prim(stage, ARTICULATION_PRIM_PATH)
        report = PhysxSchema.PhysxContactReportAPI.Apply(articulation)
        report.CreateThresholdAttr(0.0)
        self._subscription = (
            omni.physx.get_physx_simulation_interface()
            .subscribe_contact_report_events(self._on_contact_report)
        )

    @staticmethod
    def _decode_path(encoded):
        try:
            return str(PhysicsSchemaTools.intToSdfPath(encoded))
        except (TypeError, AttributeError):
            return str(PhysicsSchemaTools.decodeSdfPath(encoded[0], encoded[1]))

    @staticmethod
    def _is_robot_path(path):
        return path.startswith(ROBOT_PRIM_PATH) or path.startswith(
            ARTICULATION_PRIM_PATH
        )

    @staticmethod
    def _is_tree_path(path):
        lowered = path.lower()
        return (
            path.startswith(TREE_ROOT_PATH)
            or path.startswith(BRANCH_BODY_PATH)
            or path.startswith(CONVEYOR_PATH)
            or path.startswith(RUNTIME_CONVEYOR_COLLIDER_PATH)
            or "/trunk/" in lowered
            or "/sticks/" in lowered
            or "/sticks02/" in lowered
        )

    def set_state(self, state):
        self.state = state

    def reset(self):
        self.detected = False
        self.robot_path = None
        self.tree_path = None

    def close(self):
        self._subscription = None

    def _on_contact_report(self, headers, _data):
        if self.detected:
            return
        for header in headers:
            if int(header.num_contact_data) <= 0:
                continue
            paths = [
                self._decode_path(header.actor0),
                self._decode_path(header.actor1),
                self._decode_path(header.collider0),
                self._decode_path(header.collider1),
            ]
            robot_paths = [path for path in paths if self._is_robot_path(path)]
            tree_paths = [path for path in paths if self._is_tree_path(path)]
            if not robot_paths or not tree_paths:
                continue
            self.detected = True
            self.robot_path = robot_paths[0]
            self.tree_path = tree_paths[0]
            print(
                f"   [PHYSX CONTACT] state={self.state}, "
                f"robot={self.robot_path}, obstacle={self.tree_path}"
            )
            return


class RobotAppleContactMonitor:
    """사과와 접촉한 gripper collider가 palm인지 손가락인지 구분한다."""

    def __init__(self, stage):
        self.state = "IDLE"
        self.palm_contacted = False
        self.finger_contacted = False
        self.palm_path = None
        self.finger_path = None
        articulation = require_prim(stage, ARTICULATION_PRIM_PATH)
        report = PhysxSchema.PhysxContactReportAPI.Apply(articulation)
        report.CreateThresholdAttr(0.0)
        self._subscription = (
            omni.physx.get_physx_simulation_interface()
            .subscribe_contact_report_events(self._on_contact_report)
        )

    @staticmethod
    def _decode_path(encoded):
        return RobotTreeContactMonitor._decode_path(encoded)

    @staticmethod
    def _is_apple_path(path):
        apple_body_path = APPLE_PATH.rsplit("/", 1)[0]
        return path.startswith(apple_body_path)

    @staticmethod
    def _gripper_collider_path(paths):
        candidates = [path for path in paths if path.startswith(GRIPPER_ROOT_PATH)]
        if not candidates:
            return None
        return max(candidates, key=len)

    def set_state(self, state):
        self.state = state

    def reset(self):
        self.palm_contacted = False
        self.finger_contacted = False
        self.palm_path = None
        self.finger_path = None

    def close(self):
        self._subscription = None

    def _on_contact_report(self, headers, _data):
        for header in headers:
            if int(header.num_contact_data) <= 0:
                continue
            paths = [
                self._decode_path(header.actor0),
                self._decode_path(header.actor1),
                self._decode_path(header.collider0),
                self._decode_path(header.collider1),
            ]
            if not any(self._is_apple_path(path) for path in paths):
                continue
            gripper_path = self._gripper_collider_path(paths)
            if gripper_path is None:
                continue
            if gripper_path.startswith(PALM_PATH):
                if not self.palm_contacted:
                    self.palm_contacted = True
                    self.palm_path = gripper_path
                    print(
                        f"   [APPLE CONTACT] state={self.state}, "
                        f"type=palm, robot={gripper_path}"
                    )
            elif not self.finger_contacted:
                self.finger_contacted = True
                self.finger_path = gripper_path
                print(
                    f"   [APPLE CONTACT] state={self.state}, "
                    f"type=finger, robot={gripper_path}"
                )


def find_robot_tree_physx_overlap(stage):
    """현재 로봇 collider와 나무·컨베이어 collider 겹침을 반환한다."""
    scene_query = omni.physx.get_physx_scene_query_interface()
    robot_root = require_prim(stage, ROBOT_PRIM_PATH)
    for prim in Usd.PrimRange(robot_root):
        if not prim.IsA(UsdGeom.Gprim) or not prim.HasAPI(UsdPhysics.CollisionAPI):
            continue
        collision = UsdPhysics.CollisionAPI(prim)
        enabled = collision.GetCollisionEnabledAttr().Get()
        if enabled is False:
            continue
        encoded = PhysicsSchemaTools.encodeSdfPath(prim.GetPath())
        tree_hit = []

        def report_hit(hit):
            paths = [str(hit.collision), str(hit.rigid_body)]
            for path in paths:
                if RobotTreeContactMonitor._is_tree_path(path):
                    tree_hit.append(path)
                    return False
            return True

        scene_query.overlap_shape(
            encoded[0], encoded[1], report_hit, False
        )
        if tree_hit:
            return str(prim.GetPath()), tree_hit[0]
    return None


def configure_joint_drives(stage):
    """팔은 위치를 잘 추종하고, 손가락은 과도한 충격 없이 닫히게 한다."""
    # 고정 설치된 base/conv D455 payload에 포함된 RigidBodyAPI를 실행
    # Stage에서 비활성화한다. Collider는 정적으로 남고 센서는 중력에 떨어지지
    # 않는다. 로봇에 장착된 hand D455는 articulation을 따라야 하므로 제외한다.
    fixed_camera_bodies = 0
    for camera_root_path in FIXED_CAMERA_ROOT_PATHS:
        camera_root = require_prim(stage, camera_root_path)
        camera_body_count = 0
        for prim in Usd.PrimRange(camera_root):
            rigid_body_enabled = prim.GetAttribute("physics:rigidBodyEnabled")
            if (
                not prim.HasAPI(UsdPhysics.RigidBodyAPI)
                and not rigid_body_enabled.IsValid()
            ):
                continue
            if rigid_body_enabled.IsValid():
                rigid_body_enabled.Set(False)
            else:
                UsdPhysics.RigidBodyAPI(prim).GetRigidBodyEnabledAttr().Set(False)
            camera_body_count += 1
        if camera_body_count == 0:
            # NVIDIA D455 payload의 내부 schema가 instance/payload 구성 때문에
            # PrimRange에 노출되지 않는 경우가 있다. 알려진 payload 루트에 더
            # 강한 session-layer override를 작성해 동적 rigid body를 끈다.
            payload_root = stage.OverridePrim(f"{camera_root_path}/RSD455")
            rigid_body = UsdPhysics.RigidBodyAPI.Apply(payload_root)
            rigid_body.CreateRigidBodyEnabledAttr(False)
            camera_body_count = 1
        fixed_camera_bodies += camera_body_count

    # 저장된 rail_joint는 초기 state=0.0 m인데 drive target=1.283 m라서 Play
    # 직후 오른쪽으로 이동한다. 임의의 튜닝값 대신 authored 초기 state를
    # 그대로 위치 유지 target으로 사용한다.
    rail_joint_prim = require_prim(stage, RAIL_JOINT_PATH)
    rail_drive = UsdPhysics.DriveAPI.Get(rail_joint_prim, "linear")
    if not rail_drive:
        raise RuntimeError(f"레일 linear Drive가 없습니다: {RAIL_JOINT_PATH}")
    initial_rail_position = rail_joint_prim.GetAttribute(
        "state:linear:physics:position"
    ).Get()
    if initial_rail_position is None or not np.isfinite(initial_rail_position):
        raise RuntimeError(
            f"레일 초기 위치가 유효하지 않습니다: {initial_rail_position}"
        )
    rail_drive.GetTargetPositionAttr().Set(float(initial_rail_position))

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
            drive.GetStiffnessAttr().Set(GRIPPER_DRIVE_STIFFNESS)
            drive.GetDampingAttr().Set(GRIPPER_DRIVE_DAMPING)
            drive.GetMaxForceAttr().Set(GRIPPER_DRIVE_MAX_FORCE)
            gripper_count += 1

    if arm_count != len(ARM_JOINTS):
        raise RuntimeError(f"팔 Drive 수가 잘못되었습니다: {arm_count}")
    if gripper_count != len(GRIPPER_JOINTS):
        raise RuntimeError(f"그리퍼 Drive 수가 잘못되었습니다: {gripper_count}")

    print(
        f"   Drives       rail hold {float(initial_rail_position):.3f} m, "
        f"arm {arm_count}, gripper {gripper_count}"
    )
    print(
        f"   Gripper drive stiffness {GRIPPER_DRIVE_STIFFNESS:.1f}, "
        f"damping {GRIPPER_DRIVE_DAMPING:.1f}, "
        f"max force {GRIPPER_DRIVE_MAX_FORCE:.2f} N·m"
    )
    print(f"   Fixed cameras rigid bodies disabled {fixed_camera_bodies}")


def set_gripper_drive_max_force(stage, max_force):
    """11개 그리퍼 angular Drive의 런타임 최대 토크를 함께 변경한다."""
    max_force = float(max_force)
    if not np.isfinite(max_force) or max_force <= 0.0:
        raise ValueError(f"그리퍼 최대 토크가 유효하지 않습니다: {max_force}")
    root = require_prim(stage, ROBOT_PRIM_PATH)
    changed = 0
    for prim in Usd.PrimRange(root):
        if prim.GetName() not in GRIPPER_JOINTS:
            continue
        drive = UsdPhysics.DriveAPI.Get(prim, "angular")
        if not drive:
            continue
        drive.GetMaxForceAttr().Set(max_force)
        changed += 1
    if changed != len(GRIPPER_JOINTS):
        raise RuntimeError(
            f"그리퍼 Drive 최대 토크 변경 수가 잘못되었습니다: {changed}"
        )


def disable_leaf_colliders(stage):
    """잎 visual은 유지하고 authored PhysX collision만 비활성화한다."""
    disabled_paths = set()
    for root_path in (TREE_ROOT_PATH, BRANCH_BODY_PATH):
        root = require_prim(stage, root_path)
        for prim in Usd.PrimRange(root):
            if "/foli/" not in str(prim.GetPath()).lower():
                continue
            if prim.HasAPI(UsdPhysics.CollisionAPI):
                UsdPhysics.CollisionAPI(prim).GetCollisionEnabledAttr().Set(False)
                disabled_paths.add(str(prim.GetPath()))
    return len(disabled_paths)


def configure_contact_colliders(stage):
    """authored gripper collider만 사용하고 접촉 리포트를 활성화한다."""
    leaf_colliders_disabled = disable_leaf_colliders(stage)
    gripper_root = require_prim(stage, GRIPPER_ROOT_PATH)
    collider_count = 0

    rigid_links = [
        prim
        for prim in Usd.PrimRange(gripper_root)
        if prim.HasAPI(UsdPhysics.RigidBodyAPI)
    ]

    # ContactReportAPI는 articulation root에만 적용하면 자식 손가락 rigid
    # body의 접촉이 누락될 수 있다. 실제 충돌 주체인 각 gripper link에
    # 직접 적용해 apple contact에서 collider 경로를 받을 수 있게 한다.
    contact_report_body_count = 0
    for link_prim in rigid_links:
        report = PhysxSchema.PhysxContactReportAPI.Apply(link_prim)
        report.CreateThresholdAttr(0.0)
        contact_report_body_count += 1

    for link_prim in rigid_links:
        # URDF의 <collision>에서 가져온 STL만 사용한다. Visual Mesh를
        # Collider로 사용하면 형상이 지나치게 복잡해질 수 있다.
        source_prims = [
            prim
            for prim in Usd.PrimRange(
                link_prim,
                Usd.TraverseInstanceProxies(),
            )
            if prim.IsA(UsdGeom.Mesh) and "/collisions/" in str(prim.GetPath())
        ]
        if len(source_prims) != 1:
            raise RuntimeError(f"충돌 STL Mesh를 찾을 수 없습니다: {link_prim.GetPath()}")

        collider_path = link_prim.GetPath().AppendChild("runtime_collision")
        if stage.GetPrimAtPath(collider_path).IsValid():
            stage.RemovePrim(collider_path)
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

    apple_body_path = APPLE_PATH.rsplit("/", 1)[0]
    apple_body = require_prim(stage, apple_body_path)
    apple_report = PhysxSchema.PhysxContactReportAPI.Apply(apple_body)
    apple_report.CreateThresholdAttr(0.0)

    print(
        f"   Colliders    gripper {collider_count}, apple 1 "
        "(authored only; runtime duplicates removed)"
    )
    print(
        f"   Contact report gripper bodies {contact_report_body_count}, apple body 1"
    )
    print(
        f"   Leaf collision disabled {leaf_colliders_disabled} "
        "(visual-only)"
    )


def _mesh_sample_points_world(mesh_prim, xform_cache, vertices_only=False):
    """collision mesh의 vertex/edge midpoint/face center를 world 좌표로 샘플한다.

    vertices_only는 face/edge 보간을 생략해 훨씬 빠르다. 진입 중 반복 호출하는
    실시간 검사용이며, vertex는 볼록 collider의 최외곽이므로 최소 여유
    추정에는 충분하다.
    """
    mesh = UsdGeom.Mesh(mesh_prim)
    points = mesh.GetPointsAttr().Get()
    counts = mesh.GetFaceVertexCountsAttr().Get()
    indices = mesh.GetFaceVertexIndicesAttr().Get()
    if not points or not counts or not indices:
        return np.empty((0, 3), dtype=float)
    local = np.asarray(points, dtype=float)
    samples = [local]
    cursor = 0
    face_centers = []
    edge_centers = []
    if vertices_only:
        counts = ()
    for count in counts:
        face = np.asarray(indices[cursor:cursor + count], dtype=np.int64)
        cursor += count
        if face.size < 2:
            continue
        vertices = local[face]
        face_centers.append(np.mean(vertices, axis=0))
        edge_centers.extend(
            0.5 * (vertices + np.roll(vertices, -1, axis=0))
        )
    if face_centers:
        samples.append(np.asarray(face_centers, dtype=float))
    if edge_centers:
        samples.append(np.asarray(edge_centers, dtype=float))
    transform = xform_cache.GetLocalToWorldTransform(mesh_prim)
    return np.asarray(
        # np.vstack 결과의 각 행은 numpy.ndarray이므로 Gf.Vec3d 생성자와
        # 직접 매칭되지 않는다. 스칼라 3개로 풀어서 넘긴다.
        [
            transform.Transform(Gf.Vec3d(*(float(value) for value in point)))
            for point in np.vstack(samples)
        ],
        dtype=float,
    )


def compute_gripper_entry_swept_clearance(
    stage, current_tcp, apple_center, apple_radius, vertices_only=False
):
    """현재 finger collider가 TCP→apple 선분을 이동할 때 최소 여유를 계산한다.

    현재 자세에서 다시 호출하면 팔이 어떤 경로로 왔는지와 무관하게 남은
    여유를 그대로 알려준다. 진입 중 재측정하면 직선 이동 가정이 필요 없다.
    """
    xform_cache = UsdGeom.XformCache(Usd.TimeCode.Default())
    gripper_root = require_prim(stage, GRIPPER_ROOT_PATH)
    closest_clearance = float("inf")
    closest_path = None
    for prim in Usd.PrimRange(gripper_root, Usd.TraverseInstanceProxies()):
        path = str(prim.GetPath())
        if (
            not prim.IsA(UsdGeom.Mesh)
            or "/collisions/" not in path
            or "/finger_" not in path
        ):
            continue
        points = _mesh_sample_points_world(
            prim, xform_cache, vertices_only=vertices_only
        )
        if points.size == 0:
            continue
        distances = _point_to_segment_distances(
            points,
            np.asarray(current_tcp, dtype=float),
            np.asarray(apple_center, dtype=float),
        )
        clearance = float(np.min(distances) - float(apple_radius))
        if clearance < closest_clearance:
            closest_clearance = clearance
            closest_path = path
    if closest_path is None:
        raise RuntimeError("gripper authored collision mesh를 측정하지 못했습니다.")
    return closest_clearance, closest_path


def compute_gripper_entry_lever_arm(stage, current_tcp):
    """TCP에서 가장 먼 finger collider 점까지의 거리를 반환한다.

    진입 중 손목이 theta만큼 회전하면 finger collider는 최대 theta * (이 거리)
    만큼 옆으로 쓸린다. 이탈 원인을 위치와 회전으로 나눠 기록할 때 쓴다.
    """
    xform_cache = UsdGeom.XformCache(Usd.TimeCode.Default())
    gripper_root = require_prim(stage, GRIPPER_ROOT_PATH)
    current_tcp = np.asarray(current_tcp, dtype=float)
    lever = 0.0
    for prim in Usd.PrimRange(gripper_root, Usd.TraverseInstanceProxies()):
        path = str(prim.GetPath())
        if (
            not prim.IsA(UsdGeom.Mesh)
            or "/collisions/" not in path
            or "/finger_" not in path
        ):
            continue
        points = _mesh_sample_points_world(prim, xform_cache, vertices_only=True)
        if points.size == 0:
            continue
        lever = max(
            lever,
            float(np.max(np.linalg.norm(points - current_tcp, axis=1))),
        )
    if lever <= 0.0:
        raise RuntimeError("gripper finger collider 지렛대를 측정하지 못했습니다.")
    return lever


def point_to_line_distance(point, line_point, line_direction):
    """점과 무한 직선 사이의 수직거리를 반환한다."""
    point = np.asarray(point, dtype=float)
    line_point = np.asarray(line_point, dtype=float)
    direction = np.asarray(line_direction, dtype=float)
    norm = float(np.linalg.norm(direction))
    if norm <= 1e-12:
        raise ValueError("직선 방향 벡터가 0입니다.")
    direction = direction / norm
    delta = point - line_point
    return float(np.linalg.norm(delta - np.dot(delta, direction) * direction))


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
    global _CONVEYOR_PLANNING_GEOMETRY

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

    root_minimum = np.array(root_box.GetMin(), dtype=float)
    root_maximum = np.array(root_box.GetMax(), dtype=float)
    _CONVEYOR_PLANNING_GEOMETRY = {
        "surface_center": collider_center.copy(),
        "surface_size": collider_size.copy(),
        "root_minimum": root_minimum,
        "root_maximum": root_maximum,
        "travel_axis": travel_axis,
        "side_axis": side_axis,
        "side_inset": float(side_inset),
    }

    # TCP가 사과 중심에 위치하므로, 사과 반높이와 작은 낙하 여유를 더한다.
    start[2] = surface_z + 0.5 * apple_size[2] + RELEASE_CLEARANCE_M
    outside[2] = start[2]
    _CONVEYOR_PLANNING_GEOMETRY["place"] = start.copy()
    _CONVEYOR_PLANNING_GEOMETRY["place_above"] = start + np.array(
        [0.0, 0.0, PLACE_APPROACH_HEIGHT_M], dtype=float
    )
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


# ══════════════════════════════════════════════════════════════
# TCP 및 Palm 자세
# ══════════════════════════════════════════════════════════════
def make_approach_rotation(robot_position, apple_position):
    """gripper_frame의 접근축(+Y)이 월드 +Z를 향하도록 자세를 만든다."""
    horizontal = np.array(
        [
            apple_position[0] - robot_position[0],
            apple_position[1] - robot_position[1],
            0.0,
        ]
    )
    x_axis = normalized(horizontal)
    y_axis = np.array([0.0, 0.0, 1.0])
    z_axis = normalized(np.cross(x_axis, y_axis))
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


def compute_link6_to_palm(stage):
    """조립된 USD에서 link_6 → palm 고정변환을 읽는다."""
    cache = UsdGeom.XformCache(Usd.TimeCode.Default())
    link_matrix = cache.GetLocalToWorldTransform(require_prim(stage, LINK6_PATH))
    palm_matrix = cache.GetLocalToWorldTransform(require_prim(stage, PALM_PATH))

    link_position = np.asarray(link_matrix.ExtractTranslation(), dtype=float)
    palm_position = np.asarray(palm_matrix.ExtractTranslation(), dtype=float)
    link_rotation = quat_to_rot_matrix(
        gf_quat_to_numpy(link_matrix.ExtractRotationQuat())
    )
    palm_rotation = quat_to_rot_matrix(
        gf_quat_to_numpy(palm_matrix.ExtractRotationQuat())
    )
    rotation = link_rotation.T @ palm_rotation
    translation = link_rotation.T @ (palm_position - link_position)
    print(f"   Palm offset  translation {vec(translation)}")
    print(
        f"   Grasp center palm +Y {PALM_TO_TCP[1]:.4f} m, "
        f"nominal palm/apple gap {PALM_CONTACT_CLEARANCE_M:.4f} m"
    )
    return translation, rotation


def tcp_target_to_link6(
    tcp_position,
    palm_rotation,
    link6_to_palm_translation,
    link6_to_palm_rotation,
):
    """원하는 물리 TCP 자세를 Lula/RMPflow의 link_6 목표로 변환한다."""
    tcp_position = np.asarray(tcp_position, dtype=float)
    palm_rotation = np.asarray(palm_rotation, dtype=float)
    palm_position = tcp_position - palm_rotation @ PALM_TO_TCP
    link_rotation = palm_rotation @ np.asarray(link6_to_palm_rotation).T
    link_position = palm_position - link_rotation @ np.asarray(
        link6_to_palm_translation, dtype=float
    )
    return link_position, link_rotation


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
        "ENTER_SLOW",
        "GRASP",
        "TWIST",
        "PULL",
        "RETREAT",
        "TREE_EXIT",
        "CLEAR_UP",
        "NEUTRAL_TRANSFER",
        "CONVEYOR_OUTSIDE_HIGH",
        "TO_BELT",
        "ALIGN_DOWN",
        "PLACE_ABOVE",
        "VERTICAL_DESCENT",
        "RELEASE",
        "LIFT",
        "EXIT",
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
        # PULL 뒤에는 접근축의 정확한 반대 방향으로 먼저 나무 밖까지 빠진다.
        # 기존 대각선 RETREAT은 가지 근처에서 수평·수직 이동을 섞어 로봇 링크가
        # 나무를 쓸 수 있었으므로, 수직 상승은 CLEAR_UP에서 별도로 수행한다.
        retreat = apple_center - approach_direction * RETREAT_DISTANCE_M
        retreat_steps = max(
            MIN_MOVE_STEPS,
            int(np.ceil(np.linalg.norm(retreat - pull) / TCP_STEP_M)),
        )
        place = np.asarray(conveyor_start, dtype=float)
        outside = np.asarray(conveyor_outside, dtype=float)
        place_above = place + np.array([0.0, 0.0, PLACE_APPROACH_HEIGHT_M])
        safe_z = max(
            retreat[2] + RETREAT_HEIGHT_M,
            float(conveyor_top_z) + SAFE_CARRY_CLEARANCE_M,
            place_above[2],
        )
        clear_up = retreat.copy()
        clear_up[2] = safe_z
        conveyor_outside_high = outside.copy()
        conveyor_outside_high[2] = place_above[2]
        # CLEAR_UP→컨베이어 바깥의 2 m급 대각선을 둘로 나눈다. 첫 구간은
        # 나무에서 충분히 올라온 높이를 유지해 수평 이송하고, 둘째 구간에서만
        # 컨베이어 바깥의 접근 높이로 내려간다. joint-space neutral 값은 아직
        # TBD이므로 여기서는 두 끝점에서 계산되는 Cartesian 중간점만 사용한다.
        neutral_transfer = 0.5 * (clear_up + conveyor_outside_high)
        neutral_transfer[2] = clear_up[2]
        # 사과를 놓은 직후 측면으로 빠지면 열린 손가락이 사과를 쓸어
        # 친다. 먼저 같은 X/Y에서 짧게 수직 상승한 뒤 측면으로 이동한다.
        place_lift = place + np.array([0.0, 0.0, PLACE_VERTICAL_LIFT_M])
        place_exit = conveyor_outside_high.copy()

        approach_steps = int(
            np.clip(
                np.linalg.norm(pregrasp - current_tcp) / TCP_STEP_M,
                MIN_MOVE_STEPS,
                MAX_MOVE_STEPS,
            )
        )

        enter_slow_start = apple_center - approach_direction * ENTER_SLOW_DISTANCE_M
        specs = [
            (pregrasp, approach_rotation, approach_steps, 0.0, 0.0),
            (enter_slow_start, approach_rotation, ENTER_FAST_STEPS, 0.0, 0.0),
            (apple_center, approach_rotation, ENTER_SLOW_STEPS, 0.0, 0.0),
            (apple_center, approach_rotation, GRASP_STEPS, 0.0, 1.0),
            (apple_center, self.twisted_rotation, TWIST_STEPS, 1.0, 1.0),
            (pull, self.twisted_rotation, 120, 1.0, 1.0),
            (retreat, self.twisted_rotation, retreat_steps, 1.0, 1.0),
            # Action 경계용 무이동 상태: RETREAT이 실제 TREE_EXIT pose에
            # 도달했으므로 3초 진전 watchdog을 소모하지 않는다.
            (retreat, self.twisted_rotation, 1, 1.0, 1.0),
            (
                clear_up,
                self.twisted_rotation,
                max(
                    120,
                    int(
                        np.ceil(
                            np.linalg.norm(clear_up - retreat)
                            / PLACE_TRANSIT_STEP_M
                        )
                    ),
                ),
                1.0,
                1.0,
            ),
            (
                neutral_transfer,
                self.twisted_rotation,
                max(
                    MIN_MOVE_STEPS,
                    int(
                        np.ceil(
                            np.linalg.norm(neutral_transfer - clear_up)
                            / PLACE_TRANSIT_STEP_M
                        )
                    ),
                ),
                1.0,
                1.0,
            ),
            (
                conveyor_outside_high,
                self.twisted_rotation,
                max(
                    MIN_MOVE_STEPS,
                    int(
                        np.ceil(
                            np.linalg.norm(conveyor_outside_high - neutral_transfer)
                            / PLACE_TRANSIT_STEP_M
                        )
                    ),
                ),
                1.0,
                1.0,
            ),
            # TRANSPORT Action 종료용 무이동 상태이다. PLACE Action에서 아래
            # 방향 정렬을 시작하므로 Action 간 pose 불연속이 생기지 않는다.
            (conveyor_outside_high, self.twisted_rotation, 1, 1.0, 1.0),
            # 컨베이어에서 떨어진 높은 위치에서만 그리퍼를 아래로 돌린다.
            (
                conveyor_outside_high,
                self.place_rotation,
                PLACE_ROTATE_STEPS,
                1.0,
                1.0,
            ),
            # 상판 위까지는 별도의 수평 이송 속도를 적용한다.
            (
                place_above,
                self.place_rotation,
                max(
                    MIN_MOVE_STEPS,
                    int(
                        np.ceil(
                            np.linalg.norm(place_above - conveyor_outside_high)
                            / PLACE_TRANSIT_STEP_M
                        )
                    ),
                ),
                1.0,
                1.0,
            ),
            # 0.5 mm/step은 마지막 수직 하강 구간에만 사용한다.
            (
                place,
                self.place_rotation,
                max(
                    MIN_MOVE_STEPS,
                    int(
                        np.ceil(
                            np.linalg.norm(place - place_above)
                            / PLACE_DESCENT_STEP_M
                        )
                    ),
                ),
                1.0,
                1.0,
            ),
            (place, self.place_rotation, RELEASE_STEPS, 1.0, 0.0),
            (place_lift, self.place_rotation, PLACE_LIFT_STEPS, 0.0, 0.0),
            (
                place_exit,
                self.place_rotation,
                max(
                    MIN_MOVE_STEPS,
                    int(
                        np.ceil(
                            np.linalg.norm(place_exit - place_lift)
                            / PLACE_TRANSIT_STEP_M
                        )
                    ),
                ),
                0.0,
                0.0,
            ),
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
        if self.NAMES[self.state] == "ALIGN_DOWN":
            palm_forward = self.place_rotation[:, 1]
            palm_side = self.place_rotation[:, 0]
            print(
                f"   [ALIGN_DOWN] Palm +Y(접근축) {vec(palm_forward)}, "
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

    def advance(self, actual_position, actual_rotation, completion_allowed=True):
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
            or not completion_allowed
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

    def complete_current_on_contact(self, actual_position, actual_rotation):
        """저속 진입 중 palm 접촉 위치를 GRASP 유지 pose로 확정한다."""
        if self.done or self.NAMES[self.state] != "ENTER_SLOW":
            raise RuntimeError("ENTER_SLOW가 아닌 상태에서 접촉 완료를 요청했습니다.")
        self.start_position = np.asarray(actual_position, dtype=float)
        self.start_quat = rot_matrix_to_quat(actual_rotation)
        self.state += 1
        self.frame = 0
        self.settle_frame = 0
        self._print_state()


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
    global _LINK6_TO_PALM_TRANSLATION, _LINK6_TO_PALM_ROTATION

    (
        _LINK6_TO_PALM_TRANSLATION,
        _LINK6_TO_PALM_ROTATION,
    ) = compute_link6_to_palm(stage)
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
    print(f"   Lula frame   {EE_FRAME_NAME}")
    articulation_solver = ArticulationKinematicsSolver(
        robot_articulation=robot,
        kinematics_solver=lula,
        end_effector_frame_name=EE_FRAME_NAME,
    )
    return articulation_solver, lula


class ApproachUnreachableError(RuntimeError):
    """충돌 없는 pre-grasp 경로를 만들거나 실행할 수 없을 때 발생한다."""


class CollisionRiskError(ApproachUnreachableError):
    """외부 경로가 GPU planning proxy와 겹치는 경우 발생한다."""


class IkFailedError(ApproachUnreachableError):
    """외부 waypoint의 순차 IK 검증이 실패한 경우 발생한다."""


def _point_to_segment_distances(points, start, end):
    """각 점과 월드 선분 사이의 최단거리를 계산한다."""
    points = np.asarray(points, dtype=float)
    start = np.asarray(start, dtype=float)
    end = np.asarray(end, dtype=float)
    delta = end - start
    length_squared = float(np.dot(delta, delta))
    if length_squared <= 1e-12:
        return np.linalg.norm(points - start, axis=1)
    ratios = np.clip(((points - start) @ delta) / length_squared, 0.0, 1.0)
    closest = start + ratios[:, None] * delta
    return np.linalg.norm(points - closest, axis=1)


def _mesh_world_points(mesh_prim, xform_cache):
    """Mesh vertex를 현재 Stage의 world meter 좌표 배열로 변환한다."""
    points = UsdGeom.Mesh(mesh_prim).GetPointsAttr().Get()
    if not points:
        return np.empty((0, 3), dtype=float)
    transform = xform_cache.GetLocalToWorldTransform(mesh_prim)
    return np.asarray(
        [transform.Transform(Gf.Vec3d(point)) for point in points],
        dtype=float,
    )


def _voxel_proxy_centers(points, voxel_size, path_start, path_end, maximum_count):
    """경로 주변 점을 선별하고 시작 TCP와 겹치는 proxy를 제거한다."""
    if points.size == 0:
        return np.empty((0, 3), dtype=float)
    distances = _point_to_segment_distances(points, path_start, path_end)
    nearby = points[distances <= PLANNING_CORRIDOR_RADIUS_M]
    if nearby.size == 0:
        return np.empty((0, 3), dtype=float)

    voxel_keys = np.floor(nearby / float(voxel_size)).astype(np.int64)
    _unique, first_indices = np.unique(voxel_keys, axis=0, return_index=True)
    centers = nearby[first_indices]
    start_distances = np.linalg.norm(
        centers - np.asarray(path_start, dtype=float), axis=1
    )
    centers = centers[start_distances >= START_PROXY_EXCLUSION_RADIUS_M]
    if centers.size == 0:
        return np.empty((0, 3), dtype=float)
    center_distances = _point_to_segment_distances(centers, path_start, path_end)
    order = np.argsort(center_distances)
    if len(order) <= maximum_count:
        return centers[order]

    # 경로에 가장 가까운 proxy 일부를 반드시 보존하고, 나머지는 서로 가장
    # 멀리 떨어진 점을 반복 선택해 한 가지 구역에만 proxy가 몰리지 않게 한다.
    nearest_count = max(1, maximum_count // 3)
    candidate_count = min(len(order), maximum_count * 4)
    candidate_indices = order[:candidate_count]
    selected_indices = list(candidate_indices[:nearest_count])
    remaining_indices = list(candidate_indices[nearest_count:])
    while remaining_indices and len(selected_indices) < maximum_count:
        remaining = centers[remaining_indices]
        selected = centers[selected_indices]
        separations = np.linalg.norm(
            remaining[:, None, :] - selected[None, :, :], axis=2
        )
        next_offset = int(np.argmax(np.min(separations, axis=1)))
        selected_indices.append(remaining_indices.pop(next_offset))
    return centers[np.asarray(selected_indices, dtype=np.int64)]


def _visual_sphere(stage, path, position, radius):
    """PhysX collision 없이 RMPflow에만 전달할 보이지 않는 구를 만든다."""
    UsdGeom.Sphere.Define(stage, path)
    return VisualSphere(
        prim_path=path,
        position=np.asarray(position, dtype=float),
        radius=float(radius),
        visible=False,
    )


def _visual_cuboid(stage, path, position, size):
    """PhysX collision 없이 RMPflow에만 전달할 보이지 않는 상자를 만든다."""
    UsdGeom.Cube.Define(stage, path)
    return VisualCuboid(
        prim_path=path,
        position=np.asarray(position, dtype=float),
        scale=np.asarray(size, dtype=float),
        size=1.0,
        visible=False,
    )


def _create_conveyor_planning_obstacles(stage):
    """실측 컨베이어 AABB를 상판·측면·하부 프레임 box로 단순화한다.

    별도 안전거리 임계값은 아직 TBD이다. 따라서 각 box에는
    compute_conveyor_start()가 읽은 자산 경계 외의 여유를 더하지 않는다.
    """
    geometry = _CONVEYOR_PLANNING_GEOMETRY
    if geometry is None:
        raise RuntimeError(
            "컨베이어 planning geometry가 없습니다. "
            "compute_conveyor_start()를 먼저 호출하세요."
        )

    root_minimum = np.asarray(geometry["root_minimum"], dtype=float)
    root_maximum = np.asarray(geometry["root_maximum"], dtype=float)
    root_size = root_maximum - root_minimum
    root_center = 0.5 * (root_minimum + root_maximum)
    surface_center = np.asarray(geometry["surface_center"], dtype=float)
    surface_size = np.asarray(geometry["surface_size"], dtype=float)
    travel_axis = int(geometry["travel_axis"])
    side_axis = int(geometry["side_axis"])

    obstacles = [
        _visual_cuboid(
            stage,
            f"{PLANNING_OBSTACLE_ROOT_PATH}/conveyor_top",
            surface_center,
            surface_size,
        )
    ]

    # 자산 전체 AABB의 양쪽 외곽을 얇은 측면 box로 나타낸다. 두께는 이미
    # 실측 상판에서 제한한 collider 두께를 재사용하며 추가 margin은 없다.
    side_width = min(float(surface_size[2]), 0.5 * float(root_size[side_axis]))
    side_size = root_size.copy()
    side_size[side_axis] = side_width
    for label, coordinate in (
        ("negative", root_minimum[side_axis] + 0.5 * side_width),
        ("positive", root_maximum[side_axis] - 0.5 * side_width),
    ):
        side_center = root_center.copy()
        side_center[side_axis] = coordinate
        obstacles.append(
            _visual_cuboid(
                stage,
                f"{PLANNING_OBSTACLE_ROOT_PATH}/conveyor_side_{label}",
                side_center,
                side_size,
            )
        )

    # 상판 아래의 지지 구조는 실제 root AABB 안쪽에만 하나의 box로 묶는다.
    surface_bottom_z = surface_center[2] - 0.5 * surface_size[2]
    frame_top_z = min(float(root_maximum[2]), float(surface_bottom_z))
    frame_height = frame_top_z - float(root_minimum[2])
    if frame_height > 1e-4:
        frame_size = root_size.copy()
        frame_size[2] = frame_height
        frame_center = root_center.copy()
        frame_center[2] = root_minimum[2] + 0.5 * frame_height
        obstacles.append(
            _visual_cuboid(
                stage,
                f"{PLANNING_OBSTACLE_ROOT_PATH}/conveyor_frame",
                frame_center,
                frame_size,
            )
        )

    axis_name = "X" if travel_axis == 0 else "Y"
    print(
        f"   Planning     conveyor boxes {len(obstacles)} "
        f"(travel {axis_name}, authored AABB, safety margin TBD)"
    )
    return obstacles


def extract_static_planning_proxy_specs(stage):
    """reset 단위로 전송할 전체 나무 box/sphere proxy 명세를 만든다.

    반환 dimensions는 안전거리 적용 전 형상 크기이며, 수신 측은
    ``safety_margin``을 별도로 더한다. 잎과 목표 사과는 포함하지 않는다.
    """
    xform_cache = UsdGeom.XformCache(Usd.TimeCode.Default())
    bbox_cache = UsdGeom.BBoxCache(
        Usd.TimeCode.Default(),
        [UsdGeom.Tokens.default_, UsdGeom.Tokens.render, UsdGeom.Tokens.proxy],
        useExtentsHint=True,
    )
    branch_points = []
    trunk_meshes = []
    for root_path in (TREE_ROOT_PATH, BRANCH_BODY_PATH):
        root = require_prim(stage, root_path)
        for prim in Usd.PrimRange(root):
            path_text = str(prim.GetPath()).lower()
            if "/foli/" in path_text or not prim.IsA(UsdGeom.Mesh):
                continue
            if "/trunk/" in path_text:
                trunk_meshes.append(prim)
            elif (
                "/sticks/" in path_text
                or "/sticks02/" in path_text
                or "branchbody" in path_text
            ):
                branch_points.append(_mesh_world_points(prim, xform_cache))

    if not trunk_meshes:
        raise RuntimeError("planning scene용 나무 몸통 mesh를 찾지 못했습니다.")
    specs = []
    for index, trunk_mesh in enumerate(trunk_meshes):
        box = bbox_cache.ComputeWorldBound(trunk_mesh).ComputeAlignedBox()
        minimum = np.asarray(box.GetMin(), dtype=float)
        maximum = np.asarray(box.GetMax(), dtype=float)
        specs.append(
            {
                "obstacle_id": f"trunk_{index:03d}",
                "shape": "box",
                "obstacle_class": "trunk",
                "position": 0.5 * (minimum + maximum),
                "orientation_xyzw": np.array([0.0, 0.0, 0.0, 1.0]),
                "dimensions": maximum - minimum,
                "safety_margin": THICK_BRANCH_CLEARANCE_M,
            }
        )

    combined = (
        np.concatenate(branch_points, axis=0)
        if branch_points
        else np.empty((0, 3), dtype=float)
    )
    if combined.size:
        voxel_keys = np.floor(combined / BRANCH_PROXY_VOXEL_M).astype(np.int64)
        _unique, first_indices = np.unique(voxel_keys, axis=0, return_index=True)
        branch_centers = combined[np.sort(first_indices)]
    else:
        branch_centers = np.empty((0, 3), dtype=float)
    for index, center in enumerate(branch_centers):
        specs.append(
            {
                "obstacle_id": f"branch_{index:04d}",
                "shape": "sphere",
                "obstacle_class": "branch",
                "position": np.asarray(center, dtype=float),
                "orientation_xyzw": np.array([0.0, 0.0, 0.0, 1.0]),
                "dimensions": np.array(
                    [0.5 * BRANCH_PROXY_VOXEL_M, 0.0, 0.0], dtype=float
                ),
                "safety_margin": SMALL_BRANCH_CLEARANCE_M,
            }
        )
    print(
        f"   Scene proxy  trunk {len(trunk_meshes)}, "
        f"branch {len(branch_centers)}, leaf 0"
    )
    return specs


def create_planning_obstacles(stage, path_start, pregrasp_tcp, apple_center):
    """나무와 컨베이어를 planning-only proxy로 단순화한다."""
    if stage.GetPrimAtPath(PLANNING_OBSTACLE_ROOT_PATH).IsValid():
        stage.RemovePrim(PLANNING_OBSTACLE_ROOT_PATH)
    UsdGeom.Xform.Define(stage, PLANNING_OBSTACLE_ROOT_PATH)

    xform_cache = UsdGeom.XformCache(Usd.TimeCode.Default())
    bbox_cache = UsdGeom.BBoxCache(
        Usd.TimeCode.Default(),
        [UsdGeom.Tokens.default_, UsdGeom.Tokens.render, UsdGeom.Tokens.proxy],
        useExtentsHint=True,
    )
    tree_root = require_prim(stage, TREE_ROOT_PATH)
    branch_root = require_prim(stage, BRANCH_BODY_PATH)
    branch_points = []
    trunk_meshes = []

    for root in (tree_root, branch_root):
        for prim in Usd.PrimRange(root):
            path_text = str(prim.GetPath()).lower()
            if "/foli/" in path_text:
                continue
            if not prim.IsA(UsdGeom.Mesh):
                continue
            if "/trunk/" in path_text:
                trunk_meshes.append(prim)
            elif (
                "/sticks/" in path_text
                or "/sticks02/" in path_text
                or "branchbody" in path_text
            ):
                branch_points.append(_mesh_world_points(prim, xform_cache))

    obstacles = []
    trunk_bounds = []
    trunk_minimums = []
    trunk_maximums = []
    for index, trunk_mesh in enumerate(trunk_meshes):
        box = bbox_cache.ComputeWorldBound(trunk_mesh).ComputeAlignedBox()
        minimum = np.asarray(box.GetMin(), dtype=float)
        maximum = np.asarray(box.GetMax(), dtype=float)
        trunk_minimums.append(minimum)
        trunk_maximums.append(maximum)
        size = maximum - minimum + 2.0 * THICK_BRANCH_CLEARANCE_M
        center = 0.5 * (minimum + maximum)
        trunk_bounds.append(
            (
                minimum - THICK_BRANCH_CLEARANCE_M,
                maximum + THICK_BRANCH_CLEARANCE_M,
            )
        )
        obstacles.append(
            _visual_cuboid(
                stage,
                f"{PLANNING_OBSTACLE_ROOT_PATH}/trunk_{index:03d}",
                center,
                size,
            )
        )

    if not trunk_minimums:
        raise RuntimeError("나무 몸통 planning mesh를 찾지 못했습니다.")
    trunk_minimum = np.min(np.asarray(trunk_minimums), axis=0)
    trunk_maximum = np.max(np.asarray(trunk_maximums), axis=0)
    trunk_center = 0.5 * (trunk_minimum + trunk_maximum)
    trunk_half_extents = 0.5 * (trunk_maximum - trunk_minimum)

    combined_branches = (
        np.concatenate(branch_points, axis=0)
        if branch_points
        else np.empty((0, 3), dtype=float)
    )
    branch_centers = _voxel_proxy_centers(
        combined_branches,
        BRANCH_PROXY_VOXEL_M,
        path_start,
        pregrasp_tcp,
        MAX_BRANCH_PROXIES,
    )
    branch_radius = 0.5 * BRANCH_PROXY_VOXEL_M + SMALL_BRANCH_CLEARANCE_M
    for index, center in enumerate(branch_centers):
        obstacles.append(
            _visual_sphere(
                stage,
                f"{PLANNING_OBSTACLE_ROOT_PATH}/branch_{index:03d}",
                center,
                branch_radius,
            )
        )

    target_apple = _visual_sphere(
        stage,
        f"{PLANNING_OBSTACLE_ROOT_PATH}/target_apple",
        apple_center,
        TARGET_APPLE_OBSTACLE_RADIUS_M,
    )
    obstacles.append(target_apple)
    conveyor_obstacles = _create_conveyor_planning_obstacles(stage)
    obstacles.extend(conveyor_obstacles)
    print(
        f"   Planning     trunk {len(trunk_meshes)}, "
        f"branch {len(branch_centers)}, leaf 0 (visual-only), apple 1, "
        f"conveyor {len(conveyor_obstacles)}"
    )
    return (
        obstacles,
        target_apple,
        conveyor_obstacles,
        trunk_center,
        trunk_half_extents,
        np.asarray(branch_centers, dtype=float),
        float(branch_radius),
        trunk_bounds,
    )


class CollisionAwareMotion:
    """RMPflow와 planning proxy를 소유하는 한 수확 사이클의 motion policy."""

    def __init__(
        self,
        robot,
        stage,
        apple_center,
        path_start,
        pregrasp_tcp,
        link6_to_palm_translation=None,
        link6_to_palm_rotation=None,
    ):
        if link6_to_palm_translation is None or link6_to_palm_rotation is None:
            (
                link6_to_palm_translation,
                link6_to_palm_rotation,
            ) = compute_link6_to_palm(stage)
        self.link6_to_palm_translation = np.asarray(
            link6_to_palm_translation, dtype=float
        )
        self.link6_to_palm_rotation = np.asarray(
            link6_to_palm_rotation, dtype=float
        )
        self.rmpflow = RmpFlow(
            robot_description_path=str(DESCRIPTION_PATH),
            urdf_path=str(URDF_PATH),
            rmpflow_config_path=str(RMPFLOW_CONFIG_PATH),
            end_effector_frame_name=EE_FRAME_NAME,
            maximum_substep_size=RMPFLOW_MAXIMUM_SUBSTEP_S,
        )
        base_position, base_orientation = get_prim_world_pose(stage, ROBOT_BASE_PATH)
        self.rmpflow.set_robot_base_pose(base_position, base_orientation)
        self.articulation_policy = ArticulationMotionPolicy(
            robot,
            self.rmpflow,
            default_physics_dt=1.0 / 60.0,
        )
        (
            self.obstacles,
            self.target_apple,
            self.conveyor_obstacles,
            trunk_center,
            trunk_half_extents,
            self.branch_centers,
            self.branch_radius,
            self.trunk_bounds,
        ) = create_planning_obstacles(
            stage,
            path_start,
            pregrasp_tcp,
            apple_center,
        )
        outward = np.asarray(base_position, dtype=float) - np.asarray(
            trunk_center, dtype=float
        )
        outward[2] = 0.0
        if np.linalg.norm(outward) <= 1e-9:
            outward = np.array([1.0, 0.0, 0.0], dtype=float)
        else:
            outward = normalized(outward)
        self.outward = outward
        self.lateral = np.array([-outward[1], outward[0], 0.0], dtype=float)
        self.path_start = np.asarray(path_start, dtype=float)
        self.apple_center = np.asarray(apple_center, dtype=float)
        staging_tcp = np.asarray(pregrasp_tcp, dtype=float) - np.array(
            [0.0, 0.0, APPLE_OBSTACLE_RELEASE_DISTANCE_M - PREGRASP_DISTANCE_M]
        )
        self.staging_tcp = staging_tcp
        direct_clearance, direct_obstacle = self._route_tree_clearance(
            [self.path_start, staging_tcp]
        )
        self.tree_entry_required = direct_clearance <= SMALL_BRANCH_CLEARANCE_M

        # OUTSIDE waypoint는 나무 중심의 고정 방사점이 아니라 실제
        # 로봇→사과 진입선에서 처음 만나는 obstacle 경계를 기준으로 만든다.
        # 나무를 옮겨 진입선이 비어 있으면 불필요한 원거리 waypoint를 만들지
        # 않고 staging으로 직접 이동한다.
        low_route_start = self.path_start.copy()
        low_route_start[2] = staging_tcp[2]
        entry = self._first_tree_entry(low_route_start, staging_tcp)
        if self.tree_entry_required:
            if entry is None:
                entry = self._first_tree_entry(self.path_start, staging_tcp)
            if entry is None:
                raise RuntimeError(
                    "나무 진입이 감지됐지만 obstacle 경계점을 찾지 못했습니다."
                )
            entry_point, _entry_clearance, _entry_obstacle = entry
            horizontal_direction = staging_tcp - low_route_start
            horizontal_direction[2] = 0.0
            if np.linalg.norm(horizontal_direction) <= 1e-9:
                horizontal_direction = -self.outward
            else:
                horizontal_direction = normalized(horizontal_direction)
            self.outward = -horizontal_direction
            self.lateral = np.array(
                [-self.outward[1], self.outward[0], 0.0], dtype=float
            )
            self.outside_waypoint = np.asarray(entry_point, dtype=float)
            self.outside_waypoint[2] = staging_tcp[2]
            self.outside_waypoint += (
                self.outward * TREE_OUTSIDE_WAYPOINT_OFFSET_M
            )
            print(
                f"   Tree route   ENTRY required: direct clearance "
                f"{direct_clearance:.3f} m to {direct_obstacle}"
            )
        else:
            self.outside_waypoint = low_route_start
            print(
                f"   Tree route   CLEAR: direct clearance "
                f"{direct_clearance:.3f} m to {direct_obstacle}; "
                "OUTSIDE waypoint bypass"
            )
        for obstacle in self.obstacles:
            if not self.rmpflow.add_obstacle(obstacle, static=True):
                raise RuntimeError(
                    f"RMPflow planning obstacle을 추가하지 못했습니다: "
                    f"{obstacle.prim_path}"
                )
        arm_indices = [robot.get_dof_index(name) for name in ARM_JOINTS]
        current_arm = robot.get_joint_positions(
            joint_indices=np.asarray(arm_indices, dtype=np.int32)
        )
        if current_arm is not None:
            self.rmpflow.set_cspace_target(np.asarray(current_arm, dtype=float))
            print(
                "   RMPflow      c-space target=current arm seed; "
                "transport neutral joint configuration TBD"
            )
        self.rmpflow.update_world()
        self.apple_obstacle_enabled = True
        self.conveyor_obstacles_enabled = True
        print(f"   RMPflow      frame {EE_FRAME_NAME}, obstacles {len(self.obstacles)}")
        print(f"   Outside TCP  {vec(self.outside_waypoint)}")

    @staticmethod
    def _point_box_clearance(point, minimum, maximum):
        """점과 axis-aligned box 사이 signed 거리를 반환한다."""
        point = np.asarray(point, dtype=float)
        minimum = np.asarray(minimum, dtype=float)
        maximum = np.asarray(maximum, dtype=float)
        outside = np.maximum(np.maximum(minimum - point, point - maximum), 0.0)
        if np.any(outside > 0.0):
            return float(np.linalg.norm(outside))
        return -float(np.min(np.minimum(point - minimum, maximum - point)))

    def minimum_tcp_clearance(self, point):
        """TCP와 planning proxy 사이 최소 signed 거리를 반환한다."""
        point = np.asarray(point, dtype=float)
        candidates = []
        for index, (minimum, maximum) in enumerate(self.trunk_bounds):
            candidates.append(
                (
                    self._point_box_clearance(point, minimum, maximum),
                    f"trunk_{index:03d}",
                )
            )
        if self.branch_centers.size:
            branch_clearances = (
                np.linalg.norm(self.branch_centers - point, axis=1)
                - self.branch_radius
            )
            branch_index = int(np.argmin(branch_clearances))
            candidates.append(
                (
                    float(branch_clearances[branch_index]),
                    f"branch_{branch_index:03d}",
                )
            )
        if self.apple_obstacle_enabled:
            candidates.append(
                (
                    float(
                        np.linalg.norm(point - self.apple_center)
                        - TARGET_APPLE_OBSTACLE_RADIUS_M
                    ),
                    "target_apple",
                )
            )
        return min(candidates, key=lambda item: item[0])

    def minimum_tree_clearance(self, point):
        """목표 사과를 제외한 나무 proxy와 TCP 사이 signed 거리를 구한다."""
        point = np.asarray(point, dtype=float)
        candidates = []
        for index, (minimum, maximum) in enumerate(self.trunk_bounds):
            candidates.append(
                (
                    self._point_box_clearance(point, minimum, maximum),
                    f"trunk_{index:03d}",
                )
            )
        if self.branch_centers.size:
            branch_clearances = (
                np.linalg.norm(self.branch_centers - point, axis=1)
                - self.branch_radius
            )
            branch_index = int(np.argmin(branch_clearances))
            candidates.append(
                (
                    float(branch_clearances[branch_index]),
                    f"branch_{branch_index:03d}",
                )
            )
        return min(candidates, key=lambda item: item[0])

    @staticmethod
    def _segment_samples(route_points):
        """proxy voxel보다 촘촘한 간격으로 경로 선분을 표본화한다."""
        samples = []
        for start, end in zip(route_points[:-1], route_points[1:]):
            start = np.asarray(start, dtype=float)
            end = np.asarray(end, dtype=float)
            distance = float(np.linalg.norm(end - start))
            count = max(2, int(np.ceil(distance / BRANCH_PROXY_VOXEL_M)) + 1)
            samples.extend(
                start + alpha * (end - start)
                for alpha in np.linspace(0.0, 1.0, count)
            )
        return samples

    def _route_tree_clearance(self, route_points):
        """경로와 목표 사과를 제외한 나무 proxy 사이 최소 여유를 구한다."""
        clearances = [
            self.minimum_tree_clearance(point)
            for point in self._segment_samples(route_points)
        ]
        return min(clearances, key=lambda item: item[0])

    def _first_tree_entry(self, start, end):
        """start→end에서 나무 안전거리 안으로 처음 들어가는 점을 찾는다."""
        for point in self._segment_samples([start, end]):
            clearance, obstacle_name = self.minimum_tree_clearance(point)
            if clearance <= SMALL_BRANCH_CLEARANCE_M:
                return point, clearance, obstacle_name
        return None

    def _route_clearance(self, route_points):
        """선분들을 표본화해 planning proxy와의 최소 TCP 여유를 구한다."""
        samples = self._segment_samples(route_points)
        clearances = [self.minimum_tcp_clearance(point) for point in samples]
        return min(clearances, key=lambda item: item[0])

    def outside_route_candidates(self):
        """가지 proxy 여유를 확보한 바깥쪽 고점→저점 후보를 만든다."""
        if not self.tree_entry_required:
            return []
        definitions = [
            ("direct", 0.0, 0.0),
            ("+side", 0.0, RMPFLOW_REPLAN_OFFSET_M),
            ("-side", 0.0, -RMPFLOW_REPLAN_OFFSET_M),
            ("extra outward", RMPFLOW_REPLAN_OFFSET_M, 0.0),
        ]
        candidates = []
        for name, outward_offset, lateral_offset in definitions:
            low = (
                self.outside_waypoint
                + self.outward * outward_offset
                + self.lateral * lateral_offset
            )
            adjustment = 0.0
            for _attempt in range(4):
                high = low.copy()
                # 초기 TCP 높이(약 2.5 m)를 그대로 사용하면 M0617의 외측
                # 작업반경을 벗어날 수 있다. 사과 높이와 같은 저점 +0.30 m를
                # 바깥 정렬 고점으로 사용하고, 이후 외측에서 수직 하강한다.
                high[2] = low[2] + APPLE_OBSTACLE_RELEASE_DISTANCE_M
                clearance, obstacle_name = self._route_clearance(
                    [self.path_start, high, low]
                )
                if clearance >= SMALL_BRANCH_CLEARANCE_M:
                    break
                low = low + self.outward * RMPFLOW_REPLAN_OFFSET_M
                adjustment += RMPFLOW_REPLAN_OFFSET_M
            else:
                print(
                    f"   Outside cand {name:13s} REJECTED: "
                    f"clearance {clearance:.3f} m to {obstacle_name}"
                )
                continue

            if any(
                np.linalg.norm(low - candidate["low"]) < TARGET_POSITION_TOLERANCE_M
                for candidate in candidates
            ):
                continue
            print(
                f"   Outside cand {name:13s} low {vec(low)}, high {vec(high)}, "
                f"clearance {clearance:.3f} m to {obstacle_name}, "
                f"outward adjust {adjustment:.2f} m"
            )
            candidates.append(
                {
                    "name": name,
                    "high": high,
                    "low": low,
                    "clearance": clearance,
                }
            )
        return candidates

    def set_target(self, position, rotation):
        position = np.asarray(position, dtype=float)
        geometry = _CONVEYOR_PLANNING_GEOMETRY
        in_place_corridor = False
        if geometry is not None:
            place = np.asarray(geometry["place"], dtype=float)
            place_above = np.asarray(geometry["place_above"], dtype=float)
            in_place_corridor = (
                float(np.linalg.norm(position[:2] - place[:2])) <= 1e-6
                and position[2] <= place_above[2] + 1e-6
            )
        self._set_conveyor_obstacles_enabled(not in_place_corridor)
        link_position, link_rotation = tcp_target_to_link6(
            position,
            rotation,
            self.link6_to_palm_translation,
            self.link6_to_palm_rotation,
        )
        self.rmpflow.set_end_effector_target(
            link_position,
            rot_matrix_to_quat(link_rotation),
        )

    def _set_conveyor_obstacles_enabled(self, enabled):
        """배치 수직 통로에서만 RMPflow proxy를 열고 PhysX 감시는 유지한다."""
        enabled = bool(enabled)
        if enabled == self.conveyor_obstacles_enabled:
            return
        operation = (
            self.rmpflow.enable_obstacle
            if enabled
            else self.rmpflow.disable_obstacle
        )
        for obstacle in self.conveyor_obstacles:
            if not operation(obstacle):
                action = "활성화" if enabled else "해제"
                raise RuntimeError(
                    f"컨베이어 planning obstacle을 {action}하지 못했습니다: "
                    f"{obstacle.prim_path}"
                )
        self.conveyor_obstacles_enabled = enabled
        status = "enabled" if enabled else "disabled for vertical place corridor"
        print(
            f"   Planning     conveyor obstacles {status}; "
            "robot-conveyor PhysX contact guard remains active"
        )

    def next_action(self):
        self.rmpflow.update_world()
        return self.articulation_policy.get_next_articulation_action()

    def disable_target_apple(self):
        if self.apple_obstacle_enabled:
            if not self.rmpflow.disable_obstacle(self.target_apple):
                raise RuntimeError("목표 사과 planning obstacle을 해제하지 못했습니다.")
            self.rmpflow.update_world()
            self.apple_obstacle_enabled = False
            print(
                "   Planning     target apple obstacle disabled at staging "
                "for +Z pregrasp"
            )


def apply_gripper_positions(robot, gripper_indices, targets):
    """11개 gripper 관절에 검증된 위치 배열을 명령한다."""
    targets = np.asarray(targets, dtype=float)
    if targets.shape != (len(GRIPPER_JOINTS),) or not np.all(np.isfinite(targets)):
        raise ValueError(f"그리퍼 목표 배열이 유효하지 않습니다: {targets}")
    robot.apply_action(
        ArticulationAction(
            joint_positions=targets,
            joint_indices=np.asarray(gripper_indices, dtype=np.int32),
        )
    )


def apply_gripper_target(robot, gripper_indices, close_ratio, open_positions=None):
    """0.0=open, 1.0=closed 비율로 11개 그리퍼 관절을 명령한다."""
    open_positions = (
        GRIPPER_OPEN
        if open_positions is None
        else np.asarray(open_positions, dtype=float)
    )
    targets = open_positions + close_ratio * (GRIPPER_CLOSED - open_positions)
    apply_gripper_positions(robot, gripper_indices, targets)


def move_arm_to_pregrasp(
    world,
    robot,
    lula_solver,
    collision_motion,
    gripper_indices,
    pregrasp_tcp,
    approach_rotation,
    max_physics_steps=0,
    contact_guard=None,
    external_waypoints=None,
    external_waypoint_rotations=None,
    execution_guard=None,
    pause_callback=None,
    resume_callback=None,
):
    """사과 obstacle staging을 거쳐 충돌 없는 pregrasp 경로를 실행한다."""
    lateral_axis = np.asarray(approach_rotation[:, 2], dtype=float)
    # 개인 PC planner 규약: staging/pre-grasp/사과 진입은 항상 world +Z.
    approach_axis = np.array([0.0, 0.0, 1.0], dtype=float)
    release_offset = APPLE_OBSTACLE_RELEASE_DISTANCE_M - PREGRASP_DISTANCE_M
    if release_offset <= 0.0:
        raise RuntimeError(
            "사과 obstacle release 거리는 pregrasp 거리보다 커야 합니다."
        )
    staging_tcp = np.asarray(pregrasp_tcp) - approach_axis * release_offset
    extra_below = approach_axis * -0.05
    side_positive = (
        staging_tcp
        + lateral_axis * RMPFLOW_REPLAN_OFFSET_M
        + extra_below
    )
    side_negative = (
        staging_tcp
        - lateral_axis * RMPFLOW_REPLAN_OFFSET_M
        + extra_below
    )
    route_candidates = [
        ("direct", [staging_tcp]),
        ("replan +side", [side_positive, staging_tcp]),
        ("replan -side", [side_negative, staging_tcp]),
    ]
    physics_steps = 0

    def follow_waypoint(
        route_name,
        waypoint_index,
        waypoint_count,
        waypoint,
        target_rotation,
        position_tolerance=TARGET_POSITION_TOLERANCE_M,
        orientation_tolerance=TARGET_ORIENTATION_TOLERANCE_DEG,
    ):
        nonlocal physics_steps
        collision_motion.set_target(waypoint, target_rotation)
        # 수렴 판정이 촘촘해지면 진전 판정도 같은 비율로 촘촘해야 한다.
        # 그렇지 않으면 목표에 근접하는 동안의 작은 개선이 진전으로 잡히지
        # 않아 정체로 오판된다. 기본 허용오차에서는 기존 RMPFLOW_STALL_*
        # 값과 정확히 같아진다.
        position_progress_delta = 0.2 * position_tolerance
        orientation_progress_delta = orientation_tolerance / 3.0
        best_position_error = float("inf")
        best_orientation_error = float("inf")
        steps_without_progress = 0
        for frame in range(RMPFLOW_SEGMENT_STEPS):
            if execution_guard is not None:
                execution_guard()
            if not simulation_app.is_running():
                return None
            if max_physics_steps > 0 and physics_steps >= max_physics_steps:
                return None
            pause_reported = False
            while not world.is_playing():
                if execution_guard is not None:
                    execution_guard()
                if world.is_stopped() or not simulation_app.is_running():
                    return None
                if not pause_reported and pause_callback is not None:
                    pause_callback()
                    pause_reported = True
                world.step(render=not args.headless)
            if pause_reported and resume_callback is not None:
                resume_callback()

            if contact_guard is not None and contact_guard():
                raise ApproachUnreachableError(
                    "pre-grasp transit 중 목표 사과 stem joint가 파손됐습니다."
                )

            action = collision_motion.next_action()
            positions = action.joint_positions
            if positions is None or not np.all(np.isfinite(positions)):
                raise ApproachUnreachableError(
                    "RMPflow가 유효한 관절 목표를 생성하지 못했습니다."
                )
            robot.apply_action(action)
            apply_gripper_target(robot, gripper_indices, 0.0)
            world.step(render=not args.headless)
            physics_steps += 1
            if world.is_stopped():
                return None

            actual_tcp, actual_rotation = current_tcp_pose(robot)
            position_error = float(np.linalg.norm(waypoint - actual_tcp))
            orientation_error = rotation_error_deg(
                actual_rotation, target_rotation
            )
            progressed = False
            if (
                position_error
                <= best_position_error - position_progress_delta
            ):
                best_position_error = position_error
                progressed = True
            if (
                orientation_error
                <= best_orientation_error - orientation_progress_delta
            ):
                best_orientation_error = orientation_error
                progressed = True
            if progressed:
                steps_without_progress = 0
            else:
                steps_without_progress += 1
            if (
                position_error <= position_tolerance
                and orientation_error <= orientation_tolerance
            ):
                print(
                    f"   [TRANSIT ] {route_name} "
                    f"{waypoint_index}/{waypoint_count} 도달: "
                    f"position {position_error:.4f} m, "
                    f"rotation {orientation_error:.2f} deg"
                )
                return True
            if steps_without_progress >= RMPFLOW_STALL_STEPS:
                error_vector = np.asarray(waypoint) - actual_tcp
                clearance, obstacle_name = collision_motion.minimum_tcp_clearance(
                    actual_tcp
                )
                print(
                    f"   [STALLED ] {route_name}: "
                    f"position {position_error:.4f} m, "
                    f"rotation {orientation_error:.2f} deg, "
                    f"error xyz {vec(error_vector)}, "
                    f"TCP clearance {clearance:.3f} m to {obstacle_name}"
                )
                return False
            if frame == 0 or (frame + 1) % 60 == 0:
                print(
                    f"   TRANSIT   {route_name:12s} "
                    f"{frame + 1:3d}/{RMPFLOW_SEGMENT_STEPS} "
                    f"position {position_error:.4f} m, "
                    f"rotation {orientation_error:.2f} deg"
                )
        return False

    def outside_candidate_has_ik(candidate, current_rotation):
        """현재 관절 자세를 seed로 바깥 후보의 세 자세를 순차 검사한다."""
        arm_indices = np.asarray(
            [robot.get_dof_index(name) for name in ARM_JOINTS],
            dtype=np.int32,
        )
        warm_start = robot.get_joint_positions(joint_indices=arm_indices)
        if warm_start is None:
            raise ApproachUnreachableError(
                "바깥 waypoint IK 검사 전에 로봇 관절 위치를 읽지 못했습니다."
            )
        warm_start = np.asarray(warm_start, dtype=float)
        if not np.all(np.isfinite(warm_start)):
            raise ApproachUnreachableError(
                "바깥 waypoint IK warm-start 관절값이 유효하지 않습니다."
            )

        targets = [
            ("HIGH POSITION", candidate["high"], current_rotation),
            ("HIGH ALIGN", candidate["high"], approach_rotation),
            ("LOW DESCENT", candidate["low"], approach_rotation),
        ]
        for target_name, target_position, target_rotation in targets:
            link_position, link_rotation = tcp_target_to_link6(
                target_position,
                target_rotation,
                collision_motion.link6_to_palm_translation,
                collision_motion.link6_to_palm_rotation,
            )
            joint_goal, solved = lula_solver.compute_inverse_kinematics(
                frame_name=EE_FRAME_NAME,
                target_position=link_position,
                target_orientation=rot_matrix_to_quat(link_rotation),
                warm_start=warm_start,
                position_tolerance=0.005,
                orientation_tolerance=np.deg2rad(5.0),
            )
            if not solved:
                print(
                    f"   Outside IK   {candidate['name']:13s} FAILED "
                    f"at {target_name} {vec(target_position)}"
                )
                return False
            warm_start = np.asarray(joint_goal, dtype=float)
        print(f"   Outside IK   {candidate['name']:13s} OK (3 poses)")
        return True

    def external_route_has_ik(waypoints, rotations):
        """외부 waypoint의 순차 IK와 threshold 확정용 관절 지표를 기록한다."""

        def kinematic_condition_metrics(joint_positions):
            """수치 Jacobian의 최소 singular value와 condition number를 구한다.

            선형 m/s와 각속도 rad/s를 그대로 결합한 진단값이다. 단위 가중치와
            거부 임계값은 TBD이므로 현재는 로그 수집에만 사용한다.
            """
            joint_positions = np.asarray(joint_positions, dtype=float)
            epsilon = 1e-4
            _center_position, center_rotation = (
                lula_solver.compute_forward_kinematics(
                    EE_FRAME_NAME, joint_positions
                )
            )
            center_rotation = np.asarray(center_rotation, dtype=float)
            jacobian = np.empty((6, joint_positions.size), dtype=float)
            for joint_index in range(joint_positions.size):
                plus = joint_positions.copy()
                minus = joint_positions.copy()
                plus[joint_index] += epsilon
                minus[joint_index] -= epsilon
                plus_position, plus_rotation = (
                    lula_solver.compute_forward_kinematics(EE_FRAME_NAME, plus)
                )
                minus_position, minus_rotation = (
                    lula_solver.compute_forward_kinematics(EE_FRAME_NAME, minus)
                )
                jacobian[:3, joint_index] = (
                    np.asarray(plus_position, dtype=float)
                    - np.asarray(minus_position, dtype=float)
                ) / (2.0 * epsilon)
                rotation_derivative = (
                    np.asarray(plus_rotation, dtype=float)
                    - np.asarray(minus_rotation, dtype=float)
                ) / (2.0 * epsilon)
                angular_velocity_skew = rotation_derivative @ center_rotation.T
                jacobian[3:, joint_index] = np.array(
                    [
                        angular_velocity_skew[2, 1],
                        angular_velocity_skew[0, 2],
                        angular_velocity_skew[1, 0],
                    ],
                    dtype=float,
                )
            singular_values = np.linalg.svd(jacobian, compute_uv=False)
            minimum = float(singular_values[-1])
            condition = (
                float(singular_values[0] / minimum)
                if minimum > np.finfo(float).eps
                else float("inf")
            )
            return minimum, condition

        arm_indices = np.asarray(
            [robot.get_dof_index(name) for name in ARM_JOINTS], dtype=np.int32
        )
        warm_start = robot.get_joint_positions(joint_indices=arm_indices)
        if warm_start is None:
            raise ApproachUnreachableError(
                "외부 waypoint IK 검사 전에 로봇 관절 위치를 읽지 못했습니다."
            )
        warm_start = np.asarray(warm_start, dtype=float)
        if not np.all(np.isfinite(warm_start)):
            raise ApproachUnreachableError("외부 waypoint IK seed가 유효하지 않습니다.")
        for index, (waypoint, waypoint_rotation) in enumerate(
            zip(waypoints, rotations)
        ):
            link_position, link_rotation = tcp_target_to_link6(
                waypoint,
                waypoint_rotation,
                collision_motion.link6_to_palm_translation,
                collision_motion.link6_to_palm_rotation,
            )
            joint_goal, solved = lula_solver.compute_inverse_kinematics(
                frame_name=EE_FRAME_NAME,
                target_position=link_position,
                target_orientation=rot_matrix_to_quat(link_rotation),
                warm_start=warm_start,
                position_tolerance=0.005,
                orientation_tolerance=np.deg2rad(5.0),
            )
            if not solved:
                print(f"   External IK  waypoint {index + 1} FAILED {vec(waypoint)}")
                return False
            joint_goal = np.asarray(joint_goal, dtype=float)
            wrapped_delta = np.arctan2(
                np.sin(joint_goal - warm_start),
                np.cos(joint_goal - warm_start),
            )
            delta_degrees = np.rad2deg(np.abs(wrapped_delta))
            midpoint = warm_start + 0.5 * wrapped_delta
            print(
                f"   External IK  waypoint {index + 1} joint delta deg "
                f"max {np.max(delta_degrees):.2f}, rms "
                f"{np.sqrt(np.mean(delta_degrees ** 2)):.2f}, "
                "reject threshold TBD"
            )
            try:
                midpoint_minimum, midpoint_condition = (
                    kinematic_condition_metrics(midpoint)
                )
                goal_minimum, goal_condition = kinematic_condition_metrics(
                    joint_goal
                )
                print(
                    f"   External IK  waypoint {index + 1} numerical Jacobian "
                    f"mid sigma_min {midpoint_minimum:.6g}/cond "
                    f"{midpoint_condition:.3g}, goal sigma_min "
                    f"{goal_minimum:.6g}/cond {goal_condition:.3g}, "
                    "reject threshold TBD"
                )
            except (RuntimeError, ValueError, np.linalg.LinAlgError) as error:
                print(
                    f"   External IK  waypoint {index + 1} numerical Jacobian "
                    f"diagnostic unavailable: {error}"
                )
            warm_start = joint_goal
        print(f"   External IK  {len(waypoints)} waypoints OK")
        return True

    if external_waypoints is not None:
        waypoints = [np.asarray(point, dtype=float) for point in external_waypoints]
        if external_waypoint_rotations is None:
            rotations = [np.asarray(approach_rotation, dtype=float)] * len(waypoints)
        else:
            rotations = [
                np.asarray(rotation, dtype=float)
                for rotation in external_waypoint_rotations
            ]
        if not waypoints:
            raise ApproachUnreachableError("개인 PC의 APPROACH waypoint가 비어 있습니다.")
        if len(rotations) != len(waypoints):
            raise ApproachUnreachableError(
                "외부 waypoint 위치와 자세 개수가 다릅니다."
            )
        if any(point.shape != (3,) or not np.all(np.isfinite(point)) for point in waypoints):
            raise ApproachUnreachableError("개인 PC의 APPROACH waypoint가 유효하지 않습니다.")
        if any(
            rotation.shape != (3, 3)
            or not np.all(np.isfinite(rotation))
            or not np.allclose(rotation.T @ rotation, np.eye(3), atol=1e-4)
            or np.linalg.det(rotation) < 0.999
            for rotation in rotations
        ):
            raise ApproachUnreachableError(
                "개인 PC의 APPROACH waypoint orientation이 유효하지 않습니다."
            )
        if np.linalg.norm(waypoints[-1] - np.asarray(pregrasp_tcp)) > 0.01:
            raise ApproachUnreachableError(
                "외부 경로의 마지막 waypoint가 GPU pregrasp 목표와 일치하지 않습니다."
            )
        current_tcp, _ = current_tcp_pose(robot)
        clearance, obstacle_name = collision_motion._route_clearance(
            [current_tcp, *waypoints]
        )
        if clearance < 0.0:
            raise CollisionRiskError(
                f"GPU proxy 재검사에서 외부 경로가 {obstacle_name}과 "
                f"{clearance:.3f} m 겹칩니다."
            )
        if not external_route_has_ik(waypoints, rotations):
            raise IkFailedError("외부 APPROACH 경로의 순차 IK 검사에 실패했습니다.")
        print(
            f"   External plan {len(waypoints)} waypoints, "
            f"GPU clearance {clearance:.3f} m to {obstacle_name}"
        )
        for index, (waypoint, waypoint_rotation) in enumerate(
            zip(waypoints, rotations)
        ):
            final_waypoint = index == len(waypoints) - 1
            if final_waypoint:
                collision_motion.disable_target_apple()
            # 마지막 waypoint가 pre-grasp이며 여기서 swept clearance를 재고
            # 곧바로 진입하므로 정밀 허용오차를 사용한다.
            reached = follow_waypoint(
                "EXTERNAL APPROACH",
                index + 1,
                len(waypoints),
                waypoint,
                waypoint_rotation,
                position_tolerance=(
                    PREGRASP_POSITION_TOLERANCE_M
                    if final_waypoint
                    else TARGET_POSITION_TOLERANCE_M
                ),
                orientation_tolerance=(
                    PREGRASP_ORIENTATION_TOLERANCE_DEG
                    if final_waypoint
                    else TARGET_ORIENTATION_TOLERANCE_DEG
                ),
            )
            if reached is None:
                return physics_steps, False
            if not reached:
                raise ApproachUnreachableError(
                    f"외부 APPROACH waypoint {index + 1}/{len(waypoints)}에 "
                    "도달하지 못했습니다."
                )
        return physics_steps, True

    print(
        f"   Staging TCP  {vec(staging_tcp)} "
        f"({APPLE_OBSTACLE_RELEASE_DISTANCE_M:.2f} m below apple)"
    )
    outside_bypassed = not collision_motion.tree_entry_required
    outside_reached = outside_bypassed
    outside_candidates = collision_motion.outside_route_candidates()
    if outside_bypassed:
        print(
            "   [TRANSIT ] 로봇→staging 경로에 나무 obstacle이 없어 "
            "OUTSIDE SAFE 단계를 생략합니다."
        )
    for candidate_index, candidate in enumerate(outside_candidates):
        actual_tcp, actual_rotation = current_tcp_pose(robot)
        if not outside_candidate_has_ik(candidate, actual_rotation):
            continue
        if candidate_index:
            print(
                f"   [REPLAN  ] OUTSIDE {candidate['name']} 후보로 "
                "바깥 경로를 다시 생성합니다."
            )
        outside_route = [
            ("HIGH POSITION", candidate["high"], actual_rotation),
            ("HIGH ALIGN", candidate["high"], approach_rotation),
            ("LOW DESCENT", candidate["low"], approach_rotation),
        ]
        route_complete = True
        for waypoint_index, (target_name, waypoint, target_rotation) in enumerate(
            outside_route
        ):
            reached = follow_waypoint(
                f"OUTSIDE {candidate['name']} {target_name}",
                waypoint_index + 1,
                len(outside_route),
                waypoint,
                target_rotation,
            )
            if reached is None:
                return physics_steps, False
            if not reached:
                route_complete = False
                break
        if route_complete:
            collision_motion.outside_waypoint = np.asarray(
                candidate["low"], dtype=float
            )
            outside_reached = True
            break

    if not outside_reached:
        raise ApproachUnreachableError(
            "IK 가능한 나무 바깥 direct/+side/-side/extra-outward 경로가 "
            "모두 정체됐습니다. 나무 내부로 진입하지 않고 수확을 중단합니다."
        )

    staging_reached = False
    for route_index, (route_name, waypoints) in enumerate(route_candidates):
        if route_index:
            print(f"   [REPLAN  ] {route_name} waypoint로 경로를 다시 생성합니다.")
        route_complete = True
        for waypoint_index, waypoint in enumerate(waypoints):
            reached = follow_waypoint(
                f"STAGING {route_name}",
                waypoint_index + 1,
                len(waypoints),
                waypoint,
                approach_rotation,
            )
            if reached is None:
                return physics_steps, False
            if not reached:
                route_complete = False
                break
        if route_complete:
            staging_reached = True
            break
        if route_index + 1 < len(route_candidates) and not outside_bypassed:
            print(
                "   [RETRACT ] 다음 재계획 전에 나무 바깥 안전 waypoint로 "
                "후퇴합니다."
            )
            retracted = follow_waypoint(
                "RETRACT OUTSIDE",
                1,
                1,
                np.asarray(collision_motion.outside_waypoint, dtype=float),
                approach_rotation,
            )
            if retracted is None:
                return physics_steps, False
            if not retracted:
                raise ApproachUnreachableError(
                    "경로 정체 후 나무 바깥 안전 waypoint로 후퇴하지 "
                    "못했습니다. 현재 자세에서 정지합니다."
                )
        elif route_index + 1 < len(route_candidates):
            print(
                "   [REPLAN  ] 나무 obstacle이 없는 경로이므로 OUTSIDE "
                "후퇴 없이 다음 staging 후보를 시도합니다."
            )

    if not staging_reached:
        raise ApproachUnreachableError(
            "직접 경로와 양쪽 우회 경로 모두 obstacle-release staging에 "
            "도달하지 못했습니다."
        )

    collision_motion.disable_target_apple()
    pregrasp_reached = follow_waypoint(
        "PREGRASP +Z",
        1,
        1,
        np.asarray(pregrasp_tcp),
        approach_rotation,
        position_tolerance=PREGRASP_POSITION_TOLERANCE_M,
        orientation_tolerance=PREGRASP_ORIENTATION_TOLERANCE_DEG,
    )
    if pregrasp_reached is None:
        return physics_steps, False
    if pregrasp_reached:
        return physics_steps, True

    raise ApproachUnreachableError(
        "staging에서 사과 obstacle을 해제했지만 pre-grasp에 도달하지 "
        "못했습니다."
    )


def validate_planned_ik(
    fsm,
    lula_solver,
    initial_joint_positions,
    pregrasp_tcp,
    approach_rotation,
    link6_to_palm_translation=None,
    link6_to_palm_rotation=None,
):
    """로봇을 움직이기 전에 전체 경로를 순차 warm-start IK로 검사한다.

    각 목표를 홈 자세에서 독립적으로 풀면 실제 순차 경로가 가능한데도 실패할
    수 있다. 앞 목표의 관절 해를 다음 목표의 seed로 사용해 실제 FSM 순서를
    그대로 검사한다. ENTER도 포함하므로 사과 중심 진입 실패를 미리 발견한다.
    """
    if link6_to_palm_translation is None or link6_to_palm_rotation is None:
        link6_to_palm_translation = _LINK6_TO_PALM_TRANSLATION
        link6_to_palm_rotation = _LINK6_TO_PALM_ROTATION
    if link6_to_palm_translation is None or link6_to_palm_rotation is None:
        raise RuntimeError("link_6 → palm 변환이 초기화되지 않았습니다.")

    planned_targets = [
        ("PREGRASP", (pregrasp_tcp, approach_rotation, 0, 0.0, 0.0)),
        *list(zip(fsm.NAMES, fsm.specs)),
    ]
    warm_start = np.asarray(initial_joint_positions, dtype=float)
    checked = 0
    for state_name, spec in planned_targets:
        target_tcp, target_rotation, _steps, _grip0, _grip1 = spec
        link_position, link_rotation = tcp_target_to_link6(
            target_tcp,
            target_rotation,
            link6_to_palm_translation,
            link6_to_palm_rotation,
        )
        joint_goal, solved = lula_solver.compute_inverse_kinematics(
            frame_name=EE_FRAME_NAME,
            target_position=link_position,
            target_orientation=rot_matrix_to_quat(link_rotation),
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
):
    """초기 자세에서 한 번의 사과 수확을 수행한다.

    반환값이 ``restart``이면 GUI에서 Stop 후 Play가 입력된 것이다. 호출자는
    반드시 ``world.reset()``으로 PhysX handle을 다시 만든 뒤 이 함수를 새로
    호출해야 한다.
    """
    ik_solver, lula_solver = create_ik_solver(robot, stage)
    link6_to_palm_translation, link6_to_palm_rotation = compute_link6_to_palm(stage)

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

    collision_motion = CollisionAwareMotion(
        robot=robot,
        stage=stage,
        apple_center=apple_center,
        path_start=current_tcp,
        pregrasp_tcp=pregrasp_tcp,
        link6_to_palm_translation=link6_to_palm_translation,
        link6_to_palm_rotation=link6_to_palm_rotation,
    )
    transit_steps, transit_complete = move_arm_to_pregrasp(
        world=world,
        robot=robot,
        lula_solver=lula_solver,
        collision_motion=collision_motion,
        gripper_indices=gripper_indices,
        pregrasp_tcp=pregrasp_tcp,
        approach_rotation=approach_rotation,
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
        raise ApproachUnreachableError("충돌 회피 pregrasp 이동을 완료하지 못했습니다.")

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

        collision_motion.set_target(target_tcp, target_palm_rotation)
        arm_action = collision_motion.next_action()
        solved = (
            arm_action.joint_positions is not None
            and np.all(np.isfinite(arm_action.joint_positions))
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

            # 직선 RETREAT 완료 시 사과가 TCP 가까이에 실제로 따라왔는지 확인한다.
            next_state = fsm.NAMES[min(fsm.state, len(fsm.NAMES) - 1)]
            if (
                advance_status == "advanced"
                and next_state == "TREE_EXIT"
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
                    f"   RMPFLOW INVALID x{consecutive_ik_failures}: "
                    f"TCP {vec(target_tcp)}"
                )
            if consecutive_ik_failures >= MAX_CONSECUTIVE_IK_FAILURES:
                state_name = fsm.NAMES[min(fsm.state, len(fsm.NAMES) - 1)]
                safety_stop_reason = (
                    f"{state_name} 구간의 RMPflow 목표가 "
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
