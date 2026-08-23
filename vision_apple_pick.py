"""GPU PC 1용 통합 Isaac Sim 수확 서버.

카메라 발행과 M0617 제어는 반드시 같은 Isaac Sim World에서 실행해야 한다.
이 파일은 기존 ``apple_pick.py``의 검증된 물리·IK 함수를 재사용하고,
``/harvest/robot_motion`` Action Goal 단위로 동작을 나눈다.

실행 전 ``APPLEPROJ_INTERFACES_PREFIX``에는 Isaac Python 3.11로 빌드한
appleproj_interfaces의 install prefix를 지정해야 한다.
"""

import os
import queue
import sys
import threading
from dataclasses import dataclass
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
BRIDGE_ROOT = Path("/home/rokey/isaacsim/exts/isaacsim.ros2.bridge/jazzy")
INTERFACE_PREFIX_TEXT = os.environ.get("APPLEPROJ_INTERFACES_PREFIX", "")
INTERFACE_PREFIX = Path(INTERFACE_PREFIX_TEXT) if INTERFACE_PREFIX_TEXT else None
os.environ.setdefault("ROS_DOMAIN_ID", "102")


def prepare_isaac_ros_environment():
    """Isaac Python 3.11용 rclpy와 custom Action을 import할 환경을 만든다."""
    if INTERFACE_PREFIX is None or not INTERFACE_PREFIX.is_dir():
        raise RuntimeError(
            "APPLEPROJ_INTERFACES_PREFIX에 Isaac Python 3.11용 "
            "appleproj_interfaces install 경로를 지정하세요."
        )
    python_path = INTERFACE_PREFIX / "lib/python3.11/site-packages"
    required_paths = [BRIDGE_ROOT / "lib", INTERFACE_PREFIX / "lib"]
    current = [p for p in os.environ.get("LD_LIBRARY_PATH", "").split(":") if p]
    missing = [str(p) for p in required_paths if str(p) not in current]
    if missing and os.environ.get("VISION_PICK_ENV_READY") != "1":
        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = ":".join([*missing, *current])
        env["VISION_PICK_ENV_READY"] = "1"
        os.execve(sys.executable, [sys.executable, str(Path(__file__).resolve()), *sys.argv[1:]], env)
    sys.path[:0] = [str(BRIDGE_ROOT / "rclpy"), str(python_path)]


prepare_isaac_ros_environment()

# import 시 SimulationApp을 한 번만 생성하며 main()은 실행하지 않는다.
import apple_pick as harvest
import omni.graph.core as og
import rclpy
import usdrt.Sdf
from appleproj_interfaces.action import RobotMotion
from appleproj_interfaces.msg import (
    MotionStatus,
    ObstacleProxy,
    PlanningScene,
    SimulationState,
)
from appleproj_interfaces.srv import GetPlanningScene
from geometry_msgs.msg import PoseStamped
from isaacsim.core.utils.extensions import enable_extension
from pxr import Usd, UsdGeom
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy


MOTION_SEQUENCE = [
    RobotMotion.Goal.APPROACH,
    RobotMotion.Goal.GRASP,
    RobotMotion.Goal.TWIST,
    RobotMotion.Goal.PULL,
    RobotMotion.Goal.TRANSPORT,
    RobotMotion.Goal.PLACE,
    RobotMotion.Goal.RELEASE,
    RobotMotion.Goal.RETRACT,
]
STOP_STATE = {
    RobotMotion.Goal.GRASP: "TWIST",
    RobotMotion.Goal.TWIST: "PULL",
    RobotMotion.Goal.PULL: "RETREAT",
    RobotMotion.Goal.TRANSPORT: "TO_BELT",
    RobotMotion.Goal.PLACE: "RELEASE",
    RobotMotion.Goal.RELEASE: "LIFT",
    RobotMotion.Goal.RETRACT: "DONE",
}
ACTION_TIMEOUT_S = 3.0
ERROR_CODES = {
    "IK_FAILED": "300:IK_FAILED",
    "APPROACH_UNREACHABLE": "301:APPROACH_UNREACHABLE",
    "COLLISION_RISK": "302:COLLISION_RISK",
    # 판정 threshold는 docs/features/harvesting.md의 튜닝 항목이므로 TBD.
    "SINGULARITY_RISK": "303:SINGULARITY_RISK",
    "MOTION_TIMEOUT": "304:MOTION_TIMEOUT",
    "STEM_NOT_BROKEN": "305:STEM_NOT_BROKEN",
    "GOAL_REJECTED": "306:GOAL_REJECTED",
    "CANCELLED": "307:CANCELLED",
    "SIMULATION_RESET": "308:SIMULATION_RESET",
    "INVALID_TARGET_POSE": "309:INVALID_TARGET_POSE",
    "TF_UNAVAILABLE": "310:TF_UNAVAILABLE",
    "JOINT_STATE_UNAVAILABLE": "311:JOINT_STATE_UNAVAILABLE",
    "INTERNAL_ERROR": "312:INTERNAL_ERROR",
}

CAMERA_PATH = "/World/base_rsd455/RSD455/Camera_OmniVision_OV9782_Color"
CAMERA_GRAPH_PATH = "/BaseCameraRosGraph"


def _multiply_xyzw(a, b):
    x1, y1, z1, w1 = a
    x2, y2, z2, w2 = b
    value = harvest.np.array([
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2,
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
    ])
    return value / harvest.np.linalg.norm(value)


def create_base_camera_graph(stage):
    """같은 Isaac World에서 RGB-D, CameraInfo, clock과 고정 TF를 발행한다."""
    camera = harvest.require_prim(stage, CAMERA_PATH)
    if not camera.IsA(UsdGeom.Camera):
        raise RuntimeError(f"Color Camera Prim이 아닙니다: {CAMERA_PATH}")
    if stage.GetPrimAtPath(CAMERA_GRAPH_PATH).IsValid():
        raise RuntimeError(f"카메라 ROS 그래프가 이미 존재합니다: {CAMERA_GRAPH_PATH}")
    enable_extension("isaacsim.ros2.bridge")
    harvest.simulation_app.update()
    matrix = UsdGeom.XformCache().GetLocalToWorldTransform(camera)
    position = list(matrix.ExtractTranslation())
    q = matrix.ExtractRotationQuat()
    i = q.GetImaginary()
    rotation = _multiply_xyzw(
        [float(i[0]), float(i[1]), float(i[2]), float(q.GetReal())],
        [1.0, 0.0, 0.0, 0.0],
    ).tolist()
    k = og.Controller.Keys
    with Usd.EditContext(stage, stage.GetSessionLayer()):
        og.Controller.edit(
            {"graph_path": CAMERA_GRAPH_PATH, "evaluator_name": "execution",
             "pipeline_stage": og.GraphPipelineStage.GRAPH_PIPELINE_STAGE_SIMULATION},
            {
                k.CREATE_NODES: [
                    ("Tick", "omni.graph.action.OnPlaybackTick"),
                    ("Time", "isaacsim.core.nodes.IsaacReadSimulationTime"),
                    ("Clock", "isaacsim.ros2.bridge.ROS2PublishClock"),
                    ("Render", "isaacsim.core.nodes.IsaacCreateRenderProduct"),
                    ("Rgb", "isaacsim.ros2.bridge.ROS2CameraHelper"),
                    ("Depth", "isaacsim.ros2.bridge.ROS2CameraHelper"),
                    ("Info", "isaacsim.ros2.bridge.ROS2CameraInfoHelper"),
                    ("Tf", "isaacsim.ros2.bridge.ROS2PublishRawTransformTree"),
                ],
                k.CONNECT: [
                    ("Tick.outputs:tick", "Clock.inputs:execIn"),
                    ("Time.outputs:simulationTime", "Clock.inputs:timeStamp"),
                    ("Tick.outputs:tick", "Render.inputs:execIn"),
                    ("Render.outputs:execOut", "Rgb.inputs:execIn"),
                    ("Render.outputs:execOut", "Depth.inputs:execIn"),
                    ("Render.outputs:execOut", "Info.inputs:execIn"),
                    ("Render.outputs:renderProductPath", "Rgb.inputs:renderProductPath"),
                    ("Render.outputs:renderProductPath", "Depth.inputs:renderProductPath"),
                    ("Render.outputs:renderProductPath", "Info.inputs:renderProductPath"),
                    ("Tick.outputs:tick", "Tf.inputs:execIn"),
                    ("Time.outputs:simulationTime", "Tf.inputs:timeStamp"),
                ],
                k.SET_VALUES: [
                    ("Render.inputs:cameraPrim", [usdrt.Sdf.Path(CAMERA_PATH)]),
                    ("Render.inputs:width", 1280), ("Render.inputs:height", 720),
                    ("Rgb.inputs:frameId", "base_camera"),
                    ("Rgb.inputs:topicName", "/base_camera/color/image_raw"),
                    ("Rgb.inputs:type", "rgb"), ("Rgb.inputs:frameSkipCount", 1),
                    ("Depth.inputs:frameId", "base_camera"),
                    ("Depth.inputs:topicName", "/base_camera/depth/image_raw"),
                    ("Depth.inputs:type", "depth"), ("Depth.inputs:frameSkipCount", 1),
                    ("Info.inputs:frameId", "base_camera"),
                    ("Info.inputs:topicName", "/base_camera/camera_info"),
                    ("Info.inputs:frameSkipCount", 1),
                    ("Tf.inputs:topicName", "/tf_static"),
                    ("Tf.inputs:parentFrameId", "world"),
                    ("Tf.inputs:childFrameId", "base_camera"),
                    ("Tf.inputs:staticPublisher", True),
                    ("Tf.inputs:translation", position), ("Tf.inputs:rotation", rotation),
                ],
            },
        )


@dataclass
class PendingGoal:
    handle: object
    finished: threading.Event
    result: object = None


class MotionExecutionError(RuntimeError):
    def __init__(self, error_code, message):
        super().__init__(message)
        self.error_code = error_code


class RobotMotionNode(Node):
    """ROS callback에서는 요청만 보관하고 Isaac API는 메인 스레드만 사용한다."""

    def __init__(self):
        super().__init__(
            "isaac_robot_motion_server",
            parameter_overrides=[Parameter("use_sim_time", value=True)],
        )
        self.requests = queue.Queue(maxsize=1)
        self.busy = False
        self.lock = threading.Lock()
        self.reset_id = 0
        self.scene_version = 0
        self.simulation_state = SimulationState.INITIALIZING
        self.scene_message = None
        self.last_motion_failure = None
        latched_qos = QoSProfile(
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
        )
        self.state_publisher = self.create_publisher(
            SimulationState, "/simulation/state", latched_qos
        )
        self.scene_publisher = self.create_publisher(
            PlanningScene, "/planning_scene", latched_qos
        )
        self.scene_service = self.create_service(
            GetPlanningScene, "/planning_scene/get_snapshot", self.get_scene
        )
        status_qos = QoSProfile(
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
        )
        self.motion_status_subscription = self.create_subscription(
            MotionStatus,
            "/harvest/motion_status",
            self.on_motion_status,
            status_qos,
        )
        self.server = ActionServer(
            self,
            RobotMotion,
            "/harvest/robot_motion",
            execute_callback=self.execute,
            goal_callback=self.accept_goal,
            cancel_callback=lambda _goal: CancelResponse.ACCEPT,
        )

    def accept_goal(self, request):
        with self.lock:
            valid_state = self.simulation_state in (
                SimulationState.READY,
                SimulationState.PLAYING,
            )
            valid_version = (
                request.reset_id == self.reset_id
                and request.scene_version == self.scene_version
            )
            valid_waypoints = (
                request.motion_type != RobotMotion.Goal.APPROACH
                or len(request.waypoints) > 0
            )
            if (
                self.busy
                or request.motion_type not in MOTION_SEQUENCE
                or not valid_state
                or not valid_version
                or not valid_waypoints
            ):
                self.get_logger().warning(
                    "RobotMotion Goal 거부: "
                    f"busy={self.busy}, state={self.simulation_state}, "
                    f"goal version={request.reset_id}/{request.scene_version}, "
                    f"current={self.reset_id}/{self.scene_version}, "
                    f"waypoints={len(request.waypoints)}"
                )
                return GoalResponse.REJECT
            self.busy = True
        return GoalResponse.ACCEPT

    def on_motion_status(self, message):
        """개인 PC의 Goal 전 계획 실패를 기록하되 Goal은 차단하지 않는다."""
        if message.success:
            return
        with self.lock:
            self.last_motion_failure = (
                message.current_state,
                message.error_code,
                message.message,
                self.reset_id,
                self.scene_version,
            )
        self.get_logger().warning(
            "motion status 실패 기록: "
            f"state={message.current_state}, code={message.error_code}, "
            f"message={message.message}"
        )

    def execute(self, goal_handle):
        pending = PendingGoal(goal_handle, threading.Event())
        self.requests.put(pending)
        pending.finished.wait()
        with self.lock:
            self.busy = False
        return pending.result

    def publish_state(self, state, message=""):
        with self.lock:
            self.simulation_state = int(state)
            reset_id = self.reset_id
            scene_version = self.scene_version
        value = SimulationState()
        value.header.stamp = self.get_clock().now().to_msg()
        value.header.frame_id = "world"
        value.state = int(state)
        value.reset_id = int(reset_id)
        value.scene_version = int(scene_version)
        value.message = message
        self.state_publisher.publish(value)

    @staticmethod
    def _pose_stamped(position, quaternion_xyzw, stamp):
        value = PoseStamped()
        value.header.stamp = stamp
        value.header.frame_id = "world"
        value.pose.position.x = float(position[0])
        value.pose.position.y = float(position[1])
        value.pose.position.z = float(position[2])
        value.pose.orientation.x = float(quaternion_xyzw[0])
        value.pose.orientation.y = float(quaternion_xyzw[1])
        value.pose.orientation.z = float(quaternion_xyzw[2])
        value.pose.orientation.w = float(quaternion_xyzw[3])
        return value

    def publish_scene(self, reset_id, scene_version, specs, base_pose, tcp_pose):
        stamp = self.get_clock().now().to_msg()
        scene = PlanningScene()
        scene.header.stamp = stamp
        scene.header.frame_id = "world"
        scene.reset_id = int(reset_id)
        scene.scene_version = int(scene_version)
        base_position, base_quaternion_wxyz = base_pose
        tcp_position, tcp_rotation = tcp_pose
        base_xyzw = harvest.np.array(
            [
                base_quaternion_wxyz[1],
                base_quaternion_wxyz[2],
                base_quaternion_wxyz[3],
                base_quaternion_wxyz[0],
            ]
        )
        tcp_wxyz = harvest.rot_matrix_to_quat(tcp_rotation)
        tcp_xyzw = harvest.np.array(
            [tcp_wxyz[1], tcp_wxyz[2], tcp_wxyz[3], tcp_wxyz[0]]
        )
        scene.robot_base_pose = self._pose_stamped(base_position, base_xyzw, stamp)
        scene.robot_tcp_pose = self._pose_stamped(tcp_position, tcp_xyzw, stamp)
        for spec in specs:
            proxy = ObstacleProxy()
            proxy.obstacle_id = spec["obstacle_id"]
            proxy.shape = {
                "sphere": ObstacleProxy.SHAPE_SPHERE,
                "box": ObstacleProxy.SHAPE_BOX,
                "capsule": ObstacleProxy.SHAPE_CAPSULE,
            }[spec["shape"]]
            proxy.obstacle_class = {
                "trunk": ObstacleProxy.CLASS_TRUNK,
                "branch": ObstacleProxy.CLASS_BRANCH,
            }[spec["obstacle_class"]]
            position = spec["position"]
            orientation = spec["orientation_xyzw"]
            dimensions = spec["dimensions"]
            proxy.pose.position.x = float(position[0])
            proxy.pose.position.y = float(position[1])
            proxy.pose.position.z = float(position[2])
            proxy.pose.orientation.x = float(orientation[0])
            proxy.pose.orientation.y = float(orientation[1])
            proxy.pose.orientation.z = float(orientation[2])
            proxy.pose.orientation.w = float(orientation[3])
            proxy.dimensions.x = float(dimensions[0])
            proxy.dimensions.y = float(dimensions[1])
            proxy.dimensions.z = float(dimensions[2])
            proxy.safety_margin = float(spec["safety_margin"])
            scene.obstacles.append(proxy)
        with self.lock:
            self.reset_id = int(reset_id)
            self.scene_version = int(scene_version)
            self.scene_message = scene
        self.scene_publisher.publish(scene)
        self.get_logger().info(
            f"planning scene 발행: reset={reset_id}, version={scene_version}, "
            f"obstacles={len(scene.obstacles)}"
        )

    def get_scene(self, _request, response):
        with self.lock:
            scene = self.scene_message
        response.success = scene is not None
        if scene is not None:
            response.scene = scene
            response.message = "latest planning scene"
        else:
            response.message = "planning scene이 아직 준비되지 않았습니다."
        return response

    def execution_version(self):
        with self.lock:
            return self.reset_id, self.scene_version, self.simulation_state


class MotionEngine:
    """기존 FSM을 Action 단계 경계에서 정지시키는 메인 스레드 실행기."""

    def __init__(
        self,
        world,
        robot,
        stage,
        state_callback=None,
        execution_state_callback=None,
    ):
        self.world, self.robot, self.stage = world, robot, stage
        self.state_callback = state_callback
        self.execution_state_callback = execution_state_callback
        self.ik, self.lula = harvest.create_ik_solver(robot, stage)
        self.gripper_indices = [robot.get_dof_index(n) for n in harvest.GRIPPER_JOINTS]
        self.arm_indices = harvest.np.asarray(
            [robot.get_dof_index(n) for n in harvest.ARM_JOINTS],
            dtype=harvest.np.int32,
        )
        robot_position, _ = harvest.get_prim_world_pose(stage, harvest.ROBOT_BASE_PATH)
        _, apple_size = harvest.compute_apple_center(stage)
        self.conveyor = harvest.compute_conveyor_start(stage, robot_position, apple_size)
        self.expected_index = 0
        self.fsm = None
        self.collision_motion = None
        self.joint_break = harvest.JointBreakMonitor()
        self.tree_contact = harvest.RobotTreeContactMonitor(stage)
        self.gripper_drive_max_force = harvest.GRIPPER_GRASP_MAX_FORCE
        self.active_handle = None
        self.active_reset_id = None
        self.active_scene_version = None
        self.action_last_progress_time = None
        self.progress_tcp_position = None
        self.progress_tcp_rotation = None

    def close(self):
        self.joint_break.close()
        self.tree_contact.close()

    def _reset_action_sequence(self, reason):
        """실패한 Goal의 부분 FSM을 폐기하고 다음 요청을 APPROACH로 맞춘다."""
        self._set_gripper_drive_max_force(
            harvest.GRIPPER_GRASP_MAX_FORCE,
            f"RESET {reason}",
            report=True,
        )
        print(f"   Action reset {reason}: next expected APPROACH")
        self.expected_index = 0
        self.fsm = None
        self.collision_motion = None
        self.tree_contact.reset()

    def _hold_robot(self):
        """실행 실패 시 후퇴 동작 없이 현재 관절 위치를 유지한다."""
        try:
            positions = self.robot.get_joint_positions()
            if positions is None:
                return
            positions = harvest.np.asarray(positions, dtype=float)
            if not harvest.np.all(harvest.np.isfinite(positions)):
                return
            indices = harvest.np.arange(len(positions), dtype=harvest.np.int32)
            self.robot.apply_action(
                harvest.ArticulationAction(
                    joint_positions=positions,
                    joint_indices=indices,
                )
            )
        except Exception as error:
            print(f"   Robot hold warning: {error}")

    def _check_execution_guard(self):
        """cancel/reset/scene 변경과 simulation-time timeout을 공통 검사한다."""
        if self.active_handle is not None and self.active_handle.is_cancel_requested:
            raise MotionExecutionError("307:CANCELLED", "사용자가 동작을 취소했습니다.")
        if self.world.is_stopped() or not harvest.simulation_app.is_running():
            raise MotionExecutionError(
                "308:SIMULATION_RESET",
                "Isaac Sim Timeline이 Stop되었거나 simulation이 종료됐습니다.",
            )
        if self.execution_state_callback is not None:
            reset_id, scene_version, state = self.execution_state_callback()
            if (
                reset_id != self.active_reset_id
                or scene_version != self.active_scene_version
                or state in (SimulationState.STOPPED, SimulationState.INITIALIZING)
            ):
                raise MotionExecutionError(
                    "308:SIMULATION_RESET",
                    "Goal 승인 후 reset_id/scene_version 또는 simulation 상태가 "
                    "변경됐습니다.",
                )
        if self.action_last_progress_time is not None:
            position, rotation = self._current_tcp_pose()
            if self.progress_tcp_position is None:
                self.progress_tcp_position = position.copy()
                self.progress_tcp_rotation = rotation.copy()
            else:
                position_delta = float(
                    harvest.np.linalg.norm(position - self.progress_tcp_position)
                )
                rotation_delta = harvest.rotation_error_deg(
                    rotation, self.progress_tcp_rotation
                )
                if (
                    position_delta >= harvest.RMPFLOW_STALL_POSITION_DELTA_M
                    or rotation_delta >= harvest.RMPFLOW_STALL_ROTATION_DELTA_DEG
                ):
                    self.action_last_progress_time = float(self.world.current_time)
                    self.progress_tcp_position = position.copy()
                    self.progress_tcp_rotation = rotation.copy()
            elapsed = (
                float(self.world.current_time) - self.action_last_progress_time
            )
            if elapsed >= ACTION_TIMEOUT_S:
                raise MotionExecutionError(
                    "304:MOTION_TIMEOUT",
                    f"Action 단계에서 simulation time "
                    f"{ACTION_TIMEOUT_S:.1f}초 동안 유의미한 TCP 진전이 "
                    "없습니다.",
                )

    def _set_gripper_drive_max_force(self, max_force, state, report=False):
        """동작 단계에 맞춰 그리퍼 Drive 토크 한계를 갱신한다."""
        max_force = float(max_force)
        changed = not harvest.np.isclose(
            max_force, self.gripper_drive_max_force, atol=1e-9
        )
        if changed:
            harvest.set_gripper_drive_max_force(self.stage, max_force)
            self.gripper_drive_max_force = max_force
        if report:
            print(
                f"   Gripper force {state}: max {max_force:.3f} N·m/joint"
            )

    @staticmethod
    def result(success, code="", message=""):
        value = RobotMotion.Result()
        value.success, value.error_code, value.message = success, code, message
        return value

    def feedback(self, handle, state, progress):
        value = RobotMotion.Feedback()
        value.current_state, value.progress = state, float(progress)
        handle.publish_feedback(value)

    def _publish_pause(self):
        if self.state_callback is not None:
            self.state_callback(
                SimulationState.PAUSED,
                "Timeline Pause: 실행 중 Goal을 유지하고 로봇 명령을 보류합니다.",
            )

    def _publish_resume(self):
        if self.state_callback is not None:
            self.state_callback(
                SimulationState.PLAYING,
                "Timeline 재개: 보류한 Goal 실행을 계속합니다.",
            )

    def _require_arm_joint_positions(self):
        """Lula에 전달할 현재 팔 관절값과 Articulation handle을 검증한다."""
        joints = self.ik.get_joints_subset()
        if not joints.is_initialized:
            raise MotionExecutionError(
                "311:JOINT_STATE_UNAVAILABLE",
                "로봇 Articulation handle이 초기화되지 않았습니다. "
                "Isaac Sim Timeline Stop 이후에는 물리 재초기화가 필요합니다."
            )
        positions = joints.get_joint_positions()
        if positions is None:
            raise MotionExecutionError(
                "311:JOINT_STATE_UNAVAILABLE", "로봇 팔 관절 위치를 읽지 못했습니다."
            )
        positions = harvest.np.asarray(positions, dtype=float)
        expected_shape = (len(harvest.ARM_JOINTS),)
        if positions.shape != expected_shape:
            raise MotionExecutionError(
                "311:JOINT_STATE_UNAVAILABLE",
                f"로봇 팔 관절 배열 크기가 잘못되었습니다: "
                f"{positions.shape}, expected={expected_shape}"
            )
        if not harvest.np.all(harvest.np.isfinite(positions)):
            raise MotionExecutionError(
                "311:JOINT_STATE_UNAVAILABLE",
                "로봇 팔 관절 위치에 NaN 또는 Inf가 있습니다.",
            )
        return positions

    def _current_tcp_pose(self):
        """USD palm + local +Y 0.093 m로 물리 TCP pose를 한 번만 계산한다."""
        try:
            position, rotation = harvest.current_tcp_pose(self.robot)
        except Exception as error:
            raise MotionExecutionError(
                "310:TF_UNAVAILABLE",
                f"USD palm→TCP 변환을 계산하지 못했습니다: {error}",
            ) from error
        position = harvest.np.asarray(position, dtype=float)
        rotation = harvest.np.asarray(rotation, dtype=float)
        if (
            position.shape != (3,)
            or rotation.shape != (3, 3)
            or not harvest.np.all(harvest.np.isfinite(position))
            or not harvest.np.all(harvest.np.isfinite(rotation))
        ):
            raise MotionExecutionError(
                "310:TF_UNAVAILABLE", "USD palm→TCP pose가 유효하지 않습니다."
            )
        return position, rotation

    def execute(self, handle, reset_id, scene_version, simulation_state):
        request = handle.request
        if (
            request.reset_id != reset_id
            or request.scene_version != scene_version
        ):
            handle.abort()
            return self.result(
                False,
                "308:SIMULATION_RESET",
                "Goal 생성 이후 planning scene 버전이 변경됐습니다.",
            )
        if simulation_state not in (SimulationState.READY, SimulationState.PLAYING):
            handle.abort()
            return self.result(
                False,
                "306:GOAL_REJECTED",
                f"Isaac Sim 실행 상태가 준비되지 않았습니다: {simulation_state}",
            )
        if request.motion_type != MOTION_SEQUENCE[self.expected_index]:
            expected = MOTION_SEQUENCE[self.expected_index]
            self._hold_robot()
            self._reset_action_sequence("306:GOAL_REJECTED")
            handle.abort()
            return self.result(
                False,
                "306:GOAL_REJECTED",
                f"Action 단계 순서가 잘못되었습니다: "
                f"expected={expected}, received={request.motion_type}",
            )
        if request.target_pose.header.frame_id != "world":
            handle.abort()
            return self.result(
                False,
                "309:INVALID_TARGET_POSE",
                "target_pose frame_id는 world여야 합니다.",
            )
        target_position = request.target_pose.pose.position
        target_orientation = request.target_pose.pose.orientation
        target_values = harvest.np.array(
            [
                target_position.x,
                target_position.y,
                target_position.z,
                target_orientation.x,
                target_orientation.y,
                target_orientation.z,
                target_orientation.w,
            ],
            dtype=float,
        )
        if (
            not harvest.np.all(harvest.np.isfinite(target_values))
            or harvest.np.linalg.norm(target_values[3:]) <= 1e-12
        ):
            handle.abort()
            return self.result(
                False,
                "309:INVALID_TARGET_POSE",
                "target_pose 위치/자세가 유효하지 않습니다.",
            )
        self.active_handle = handle
        self.active_reset_id = int(reset_id)
        self.active_scene_version = int(scene_version)
        self.action_last_progress_time = float(self.world.current_time)
        self.progress_tcp_position = None
        self.progress_tcp_rotation = None
        try:
            self._check_execution_guard()
            if request.motion_type == RobotMotion.Goal.APPROACH:
                overlap = harvest.find_robot_tree_physx_overlap(self.stage)
                if overlap is not None:
                    raise MotionExecutionError(
                        "302:COLLISION_RISK",
                        f"실행 전 실제 PhysX collider가 겹쳐 있습니다: {overlap}",
                    )
                self._approach(handle, request.target_pose, request.waypoints)
            else:
                self._run_fsm(handle, STOP_STATE[request.motion_type])
                if request.motion_type == RobotMotion.Goal.GRASP:
                    self._report_grasp_state()
                if (
                    request.motion_type == RobotMotion.Goal.PULL
                    and not self.joint_break.broken
                ):
                    raise MotionExecutionError(
                        "305:STEM_NOT_BROKEN",
                        "PULL 완료 시점까지 사과 FixedJoint가 분리되지 않았습니다.",
                    )
        except MotionExecutionError as error:
            self._hold_robot()
            self._reset_action_sequence(error.error_code)
            if error.error_code == "307:CANCELLED":
                handle.canceled()
            else:
                handle.abort()
            return self.result(False, error.error_code, str(error))
        except harvest.CollisionRiskError as error:
            self._hold_robot()
            self._reset_action_sequence("302:COLLISION_RISK")
            handle.abort()
            return self.result(False, "302:COLLISION_RISK", str(error))
        except harvest.IkFailedError as error:
            self._hold_robot()
            self._reset_action_sequence("300:IK_FAILED")
            handle.abort()
            return self.result(False, "300:IK_FAILED", str(error))
        except harvest.ApproachUnreachableError as error:
            self._hold_robot()
            self._reset_action_sequence("301:APPROACH_UNREACHABLE")
            handle.abort()
            return self.result(False, "301:APPROACH_UNREACHABLE", str(error))
        except Exception as error:
            self._hold_robot()
            self._reset_action_sequence("312:INTERNAL_ERROR")
            handle.abort()
            return self.result(False, "312:INTERNAL_ERROR", str(error))
        finally:
            self.active_handle = None
            self.action_last_progress_time = None
            self.progress_tcp_position = None
            self.progress_tcp_rotation = None
        self.expected_index += 1
        if self.expected_index == len(MOTION_SEQUENCE):
            self._reset_action_sequence("CYCLE_COMPLETE")
        handle.succeed()
        return self.result(True, "", "동작 완료")

    def _approach(self, handle, pose, waypoint_messages):
        if self.joint_break.broken:
            raise MotionExecutionError(
                "308:SIMULATION_RESET",
                "사과 FixedJoint가 이미 분리됐습니다. 시뮬레이션을 Reset한 뒤 "
                "다시 실행하세요.",
            )
        apple = pose.pose.position
        center = harvest.np.array([apple.x, apple.y, apple.z], dtype=float)
        if not harvest.np.all(harvest.np.isfinite(center)):
            raise MotionExecutionError(
                "309:INVALID_TARGET_POSE", "사과 좌표에 NaN 또는 Inf가 있습니다."
            )
        direction = harvest.np.array([0.0, 0.0, 1.0], dtype=float)
        pregrasp = center - direction * harvest.PREGRASP_DISTANCE_M
        staging = center - direction * harvest.APPLE_OBSTACLE_RELEASE_DISTANCE_M
        external_waypoints = []
        external_rotations = []
        for waypoint in waypoint_messages:
            if waypoint.header.frame_id != "world":
                raise MotionExecutionError(
                    "309:INVALID_TARGET_POSE",
                    "모든 APPROACH waypoint frame_id는 world여야 합니다.",
                )
            p = waypoint.pose.position
            position = harvest.np.array([p.x, p.y, p.z], dtype=float)
            q = waypoint.pose.orientation
            quaternion_xyzw = harvest.np.array([q.x, q.y, q.z, q.w], dtype=float)
            norm = float(harvest.np.linalg.norm(quaternion_xyzw))
            if (
                not harvest.np.all(harvest.np.isfinite(position))
                or not harvest.np.all(harvest.np.isfinite(quaternion_xyzw))
                or norm <= 1e-12
            ):
                raise MotionExecutionError(
                    "309:INVALID_TARGET_POSE",
                    "APPROACH waypoint 위치/자세가 유효하지 않습니다.",
                )
            quaternion_xyzw /= norm
            rotation = harvest.quat_to_rot_matrix(
                harvest.np.array(
                    [
                        quaternion_xyzw[3],
                        quaternion_xyzw[0],
                        quaternion_xyzw[1],
                        quaternion_xyzw[2],
                    ]
                )
            )
            external_waypoints.append(position)
            external_rotations.append(rotation)
        if not external_waypoints:
            raise MotionExecutionError(
                "309:INVALID_TARGET_POSE", "APPROACH waypoint가 비어 있습니다."
            )
        rotation = external_rotations[-1]
        print(f"   Staging TCP  {harvest.vec(staging)} (world -Z 0.30 m)")
        print(f"   Pregrasp TCP {harvest.vec(pregrasp)} (world -Z 0.15 m)")
        planned = harvest.AppleHarvestFSM(
            pregrasp, rotation, center, rotation, direction, *self.conveyor,
            start_at_pregrasp=True,
        )
        initial = self._require_arm_joint_positions()
        if not harvest.validate_planned_ik(
            planned, self.lula, initial, pregrasp, rotation
        ):
            raise MotionExecutionError(
                "300:IK_FAILED",
                "비전 목표의 전체 수확 경로 IK 검사에 실패했습니다."
            )
        current_tcp, _current_rotation = self._current_tcp_pose()
        self.collision_motion = harvest.CollisionAwareMotion(
            robot=self.robot,
            stage=self.stage,
            apple_center=center,
            path_start=current_tcp,
            pregrasp_tcp=pregrasp,
        )
        self.joint_break.set_state("PRE_GRASP")
        self.tree_contact.reset()
        self.tree_contact.set_state("APPROACH")
        self.feedback(handle, "APPROACH", 0.1)
        def contact_guard():
            if self.tree_contact.detected:
                raise MotionExecutionError(
                    "302:COLLISION_RISK",
                    "APPROACH 중 실제 로봇 collider가 나무 collider에 접촉했습니다: "
                    f"robot={self.tree_contact.robot_path}, tree={self.tree_contact.tree_path}",
                )
            return self.joint_break.broken

        _steps, complete = harvest.move_arm_to_pregrasp(
            world=self.world,
            robot=self.robot,
            lula_solver=self.lula,
            collision_motion=self.collision_motion,
            gripper_indices=self.gripper_indices,
            pregrasp_tcp=pregrasp,
            approach_rotation=rotation,
            max_physics_steps=0,
            contact_guard=contact_guard,
            external_waypoints=external_waypoints,
            external_waypoint_rotations=external_rotations,
            execution_guard=self._check_execution_guard,
            pause_callback=self._publish_pause,
            resume_callback=self._publish_resume,
        )
        if not complete:
            if self.world.is_stopped() or not harvest.simulation_app.is_running():
                raise MotionExecutionError(
                    "308:SIMULATION_RESET", "Isaac Sim Timeline이 Stop되었습니다."
                )
            raise harvest.ApproachUnreachableError(
                "pregrasp 이동을 완료하지 못했습니다."
            )
        tcp, palm_rotation = self._current_tcp_pose()
        self.fsm = harvest.AppleHarvestFSM(
            tcp, palm_rotation, center, rotation, direction, *self.conveyor,
            start_at_pregrasp=True,
        )
        # APPROACH Action에 pre-grasp → 사과 중심 world +Z 진입을 포함한다.
        # 다음 GRASP Action은 이 자세를 유지하고 그리퍼만 폐합한다.
        self._run_fsm(handle, "GRASP")
        self.feedback(handle, "APPROACH", 1.0)

    def _report_grasp_state(self):
        actual_gripper = harvest.np.asarray(
            self.robot.get_joint_positions(
                joint_indices=harvest.np.asarray(
                    self.gripper_indices, dtype=harvest.np.int32
                )
            ),
            dtype=float,
        )
        tcp, _rotation = self._current_tcp_pose()
        apple = harvest.compute_live_prim_center(self.stage, harvest.APPLE_PATH)
        distance = float(harvest.np.linalg.norm(apple - tcp))
        max_target_error = float(
            harvest.np.max(harvest.np.abs(harvest.GRIPPER_CLOSED - actual_gripper))
        )
        print(
            f"   [GRASP CHECK] TCP-apple={distance:.4f} m, "
            f"gripper max target error={max_target_error:.4f} rad, "
            f"joint_broken={self.joint_break.broken}"
        )
        if self.joint_break.broken:
            raise MotionExecutionError(
                "302:COLLISION_RISK",
                f"사과 FixedJoint가 {self.joint_break.break_state} 중 조기 파손됐습니다.",
            )

    def _run_fsm(self, handle, stop_state):
        if self.fsm is None or self.collision_motion is None:
            raise MotionExecutionError(
                "306:GOAL_REJECTED", "APPROACH가 먼저 완료되지 않았습니다."
            )
        failures = 0
        hold_arm_positions = None
        grasp_settle_remaining = harvest.GRASP_SETTLE_STEPS
        reported_force_state = None
        while not self.fsm.done and self.fsm.NAMES[self.fsm.state] != stop_state:
            self._check_execution_guard()
            pause_reported = False
            while not self.world.is_playing():
                self._check_execution_guard()
                if not pause_reported:
                    self._publish_pause()
                    pause_reported = True
                harvest.simulation_app.update()
            if pause_reported:
                self._publish_resume()
            current_arm_positions = self._require_arm_joint_positions()
            motion_state = self.fsm.NAMES[self.fsm.state]
            self.tree_contact.set_state(motion_state)

            if motion_state in {"GRASP", "RELEASE"} and hold_arm_positions is None:
                hold_arm_positions = current_arm_positions.copy()
                if motion_state == "GRASP":
                    self._set_gripper_drive_max_force(
                        harvest.GRIPPER_GRASP_MAX_FORCE,
                        "GRASP",
                        report=True,
                    )
                    print(
                        f"   [GRASP SETTLE] arm hold for "
                        f"{harvest.GRASP_SETTLE_STEPS} steps before closing"
                    )

            if motion_state == "GRASP" and grasp_settle_remaining > 0:
                self.joint_break.set_state("GRASP_SETTLE")
                self.robot.apply_action(
                    harvest.ArticulationAction(
                        joint_positions=hold_arm_positions,
                        joint_indices=self.arm_indices,
                    )
                )
                harvest.apply_gripper_target(
                    self.robot, self.gripper_indices, 0.0
                )
                completed = (
                    harvest.GRASP_SETTLE_STEPS - grasp_settle_remaining + 1
                )
                if completed == 1 or completed % 60 == 0:
                    print(
                        f"   GRASP SETTLE {completed:3d}/"
                        f"{harvest.GRASP_SETTLE_STEPS}"
                    )
                self.feedback(
                    handle,
                    "GRASP_SETTLE",
                    completed / float(harvest.GRASP_SETTLE_STEPS),
                )
                self.world.step(render=not harvest.args.headless)
                grasp_settle_remaining -= 1
                if self.tree_contact.detected:
                    raise MotionExecutionError(
                        "302:COLLISION_RISK",
                        "GRASP_SETTLE 중 실제 로봇 collider가 나무 collider에 "
                        f"접촉했습니다: robot={self.tree_contact.robot_path}, "
                        f"tree={self.tree_contact.tree_path}",
                    )
                if self.joint_break.broken:
                    raise MotionExecutionError(
                        "302:COLLISION_RISK",
                        "사과 FixedJoint가 GRASP_SETTLE 중 조기 파손됐습니다.",
                    )
                continue

            self.joint_break.set_state(motion_state)
            target, rotation, grip = self.fsm.sample()
            if motion_state == "TWIST":
                alpha = min(
                    1.0,
                    (self.fsm.frame + 1) / float(harvest.TWIST_STEPS),
                )
                max_force = (
                    harvest.GRIPPER_GRASP_MAX_FORCE
                    + harvest.smoothstep(alpha)
                    * (
                        harvest.GRIPPER_HOLD_MAX_FORCE
                        - harvest.GRIPPER_GRASP_MAX_FORCE
                    )
                )
                self._set_gripper_drive_max_force(
                    max_force,
                    "TWIST RAMP",
                    report=self.fsm.frame in (0, harvest.TWIST_STEPS - 1),
                )
            elif motion_state in {
                "PULL",
                "RETREAT",
                "CLEAR_UP",
                "OUTSIDE",
                "ALIGN",
                "TO_BELT",
            }:
                self._set_gripper_drive_max_force(
                    harvest.GRIPPER_HOLD_MAX_FORCE,
                    motion_state,
                    report=reported_force_state != "HOLD",
                )
                reported_force_state = "HOLD"
            elif motion_state in {"RELEASE", "LIFT", "EXIT"}:
                self._set_gripper_drive_max_force(
                    harvest.GRIPPER_GRASP_MAX_FORCE,
                    motion_state,
                    report=reported_force_state != "RELEASE",
                )
                reported_force_state = "RELEASE"
            if motion_state in {"GRASP", "RELEASE"}:
                # 파지/개방 중 RMPflow의 미세 Cartesian 보정을 막고,
                # Action 시작 시점의 관절 자세를 유지한다.
                action = harvest.ArticulationAction(
                    joint_positions=hold_arm_positions,
                    joint_indices=self.arm_indices,
                )
                solved = True
            else:
                self.collision_motion.set_target(target, rotation)
                action = self.collision_motion.next_action()
                solved = (
                    action.joint_positions is not None
                    and harvest.np.all(harvest.np.isfinite(action.joint_positions))
                )
            if solved:
                self.robot.apply_action(action)
                failures = 0
                actual, actual_rotation = self._current_tcp_pose()
                if self.fsm.advance(actual, actual_rotation) == "timeout":
                    raise MotionExecutionError(
                        "304:MOTION_TIMEOUT",
                        "TCP가 목표를 제한 시간 안에 추종하지 못했습니다.",
                    )
            else:
                failures += 1
                if failures >= harvest.MAX_CONSECUTIVE_IK_FAILURES:
                    raise MotionExecutionError(
                        "300:IK_FAILED",
                        "RMPflow 관절 목표가 연속으로 유효하지 않습니다.",
                    )
            harvest.apply_gripper_target(self.robot, self.gripper_indices, grip)
            state = self.fsm.NAMES[min(self.fsm.state, len(self.fsm.NAMES) - 1)]
            self.feedback(handle, state, 0.5)
            self.world.step(render=not harvest.args.headless)
            if self.tree_contact.detected:
                raise MotionExecutionError(
                    "302:COLLISION_RISK",
                    f"{motion_state} 중 실제 로봇 collider가 나무 collider에 "
                    f"접촉했습니다: robot={self.tree_contact.robot_path}, "
                    f"tree={self.tree_contact.tree_path}",
                )
            if (
                self.joint_break.broken
                and self.joint_break.break_state not in {"TWIST", "PULL"}
            ):
                raise MotionExecutionError(
                    "302:COLLISION_RISK",
                    f"사과 FixedJoint가 {self.joint_break.break_state} 중 조기 파손됐습니다.",
                )
        self._check_execution_guard()
        self.feedback(handle, stop_state, 1.0)


def main():
    stage = harvest.open_project_stage()
    create_base_camera_graph(stage)
    harvest.configure_breakable_joint(stage)
    harvest.configure_contact_colliders(stage)
    harvest.configure_joint_drives(stage)
    world = harvest.World(
        stage_units_in_meters=1.0, physics_prim_path="/physicsScene",
        physics_dt=1.0 / 60.0, rendering_dt=1.0 / 60.0,
    )
    robot = harvest.create_robot(world)
    rclpy.init()
    node = RobotMotionNode()
    engine = MotionEngine(
        world,
        robot,
        stage,
        node.publish_state,
        node.execution_version,
    )
    executor = MultiThreadedExecutor(num_threads=2)
    executor.add_node(node)
    ros_thread = threading.Thread(target=executor.spin, daemon=True)
    ros_thread.start()
    reset_id = 1
    scene_version = 1

    def publish_current_scene():
        specs = harvest.extract_static_planning_proxy_specs(stage)
        base_pose = harvest.get_prim_world_pose(stage, harvest.ROBOT_BASE_PATH)
        tcp_pose = harvest.current_tcp_pose(robot)
        node.publish_scene(
            reset_id,
            scene_version,
            specs,
            base_pose,
            tcp_pose,
        )

    try:
        node.publish_state(SimulationState.INITIALIZING, "Stage와 물리를 초기화합니다.")
        world.play()
        world.step(render=not harvest.args.headless)
        publish_current_scene()
        node.publish_state(SimulationState.READY, "planning scene 동기화가 완료됐습니다.")
        node.publish_state(SimulationState.PLAYING, "Isaac Sim Timeline이 실행 중입니다.")
        published_state = SimulationState.PLAYING
        stopped_needs_reset = False
        while harvest.simulation_app.is_running():
            if world.is_stopped():
                if published_state != SimulationState.STOPPED:
                    node.publish_state(
                        SimulationState.STOPPED,
                        "Timeline Stop: 실행 중 Goal과 이전 계획을 폐기합니다.",
                    )
                    published_state = SimulationState.STOPPED
                stopped_needs_reset = True
                harvest.simulation_app.update()
                continue
            if not world.is_playing():
                if published_state != SimulationState.PAUSED:
                    node.publish_state(
                        SimulationState.PAUSED,
                        "Timeline Pause: Goal 실행을 일시 정지합니다.",
                    )
                    published_state = SimulationState.PAUSED
                harvest.simulation_app.update()
                continue
            if stopped_needs_reset:
                node.publish_state(
                    SimulationState.INITIALIZING,
                    "Stop 이후 Articulation과 planning scene을 재초기화합니다.",
                )
                engine.close()
                world.reset()
                engine = MotionEngine(
                    world,
                    robot,
                    stage,
                    node.publish_state,
                    node.execution_version,
                )
                world.play()
                world.step(render=not harvest.args.headless)
                reset_id += 1
                scene_version += 1
                publish_current_scene()
                node.publish_state(
                    SimulationState.READY,
                    "새 reset의 planning scene 동기화가 완료됐습니다.",
                )
                stopped_needs_reset = False
            if published_state != SimulationState.PLAYING:
                node.publish_state(
                    SimulationState.PLAYING, "Isaac Sim Timeline이 실행 중입니다."
                )
                published_state = SimulationState.PLAYING
            try:
                pending = node.requests.get_nowait()
            except queue.Empty:
                world.step(render=not harvest.args.headless)
                continue
            if world.is_stopped() or not robot.handles_initialized:
                node.get_logger().warning(
                    "Articulation handle이 해제되어 물리와 MotionEngine을 재초기화합니다."
                )
                node.publish_state(
                    SimulationState.INITIALIZING,
                    "Articulation handle 재초기화 중입니다.",
                )
                engine.close()
                world.reset()
                engine = MotionEngine(
                    world,
                    robot,
                    stage,
                    node.publish_state,
                    node.execution_version,
                )
                world.play()
                world.step(render=not harvest.args.headless)
                reset_id += 1
                scene_version += 1
                publish_current_scene()
                node.publish_state(
                    SimulationState.PLAYING,
                    "Articulation과 planning scene 재동기화가 완료됐습니다.",
                )
            pending.result = engine.execute(
                pending.handle, *node.execution_version()
            )
            pending.finished.set()
    finally:
        engine.close()
        executor.shutdown()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
        world.stop()
        harvest.simulation_app.close()


if __name__ == "__main__":
    main()
