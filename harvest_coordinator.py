"""GPU PC 1용 수확 supervisor와 RobotMotion Action Client."""

import argparse
from collections import deque
from dataclasses import dataclass
import math

import numpy as np
import rclpy
from appleproj_interfaces.action import RobotMotion
from appleproj_interfaces.msg import (
    HarvestPerceptionStatus,
    HarvestTarget,
    MotionStatus,
    PlanningScene,
    SimulationState,
)
from appleproj_interfaces.srv import GetPlanningScene
from geometry_msgs.msg import PoseStamped
from harvest_route_planner import (
    RoutePlanningError,
    approach_orientation_xyzw,
    validate_scene_version,
)
from rclpy.action import ActionClient
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy
from rclpy.time import Time
from tf2_ros import Buffer, TransformException, TransformListener


SEQUENCE = [
    RobotMotion.Goal.APPROACH,
    RobotMotion.Goal.GRASP,
    RobotMotion.Goal.TWIST,
    RobotMotion.Goal.PULL,
    RobotMotion.Goal.TRANSPORT,
    RobotMotion.Goal.PLACE,
    RobotMotion.Goal.RELEASE,
    RobotMotion.Goal.RETRACT,
]

# The physical harvest TCP is defined from the USD `palm` frame. GPU PC 1
# publishes that frame in the dynamic TF tree, so no link_6-to-TCP
# calibration or gripper_frame approximation is needed here.
TCP_FRAME = "palm"
PALM_TO_TCP_Y_M = 0.0908

# Threshold 값은 통합 시험 전까지 TBD다. 음수 sentinel은 해당 검사를
# 비활성화하며, 범위·세대·frame·timestamp 일치 검사는 항상 수행한다.
TARGET_MAX_AGE_SEC = -1.0
MIN_TARGET_CONFIDENCE = -1.0
MIN_VALID_DEPTH_RATIO = -1.0
MAX_TF_TIME_ERROR_SEC = -1.0

TARGET_TOPIC = "/harvest/target"
PERCEPTION_STATUS_TOPIC = "/harvest/perception_status"
TARGET_BATCH_DEBOUNCE_SEC = 0.05


@dataclass
class PendingTarget:
    key: tuple
    message: HarvestTarget
    center: np.ndarray
    stamp_ns: int


class HarvestCoordinator(Node):
    def __init__(self, execute, sample_count, maximum_spread):
        if int(sample_count) <= 0:
            raise ValueError("sample_count는 1 이상이어야 합니다.")
        if float(maximum_spread) < 0.0:
            raise ValueError("maximum_spread는 0 이상이어야 합니다.")
        super().__init__(
            "harvest_coordinator",
            parameter_overrides=[Parameter("use_sim_time", value=True)],
        )
        self.execute_enabled = execute
        self.sample_count = int(sample_count)
        self.samples = deque(maxlen=sample_count)
        self.target_samples = {}
        self.pending_targets = {}
        self.retry_targets = {}
        self.completed_target_keys = set()
        self.failed_once_target_keys = set()
        self.final_failed_target_keys = set()
        self._active_candidate = None
        self.maximum_spread = maximum_spread
        self.target = None
        self.failed_target = None
        self.index = 0
        self.running = False
        self.goal_handle = None
        self.planning_scene = None
        self.simulation_state = None
        self.plan_reset_id = 0
        self.plan_scene_version = 0
        self.approach_orientation = None
        self.snapshot_request_pending = False
        self.generation = 0
        self._last_tcp_lookup_failure = None
        self._sample_target_key = None
        self._active_target_key = None
        self._latest_target_stamps = {}
        self._started_target_keys = set()
        self.safety_stopped = False
        self.safety_stop_reason = None
        self.target_max_age_sec = self._optional_threshold(TARGET_MAX_AGE_SEC)
        self.minimum_target_confidence = self._optional_threshold(
            MIN_TARGET_CONFIDENCE
        )
        self.minimum_valid_depth_ratio = self._optional_threshold(
            MIN_VALID_DEPTH_RATIO
        )
        self.maximum_tf_time_error_sec = self._optional_threshold(
            MAX_TF_TIME_ERROR_SEC
        )

        latched_qos = QoSProfile(
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
        )
        self.client = ActionClient(self, RobotMotion, "/harvest/robot_motion")
        status_qos = QoSProfile(
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
        )
        self.status_publisher = self.create_publisher(
            MotionStatus, "/harvest/motion_status", status_qos
        )
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.scene_client = self.create_client(
            GetPlanningScene, "/planning_scene/get_snapshot"
        )
        self.create_subscription(
            PlanningScene, "/planning_scene", self.on_scene, latched_qos
        )
        self.create_subscription(
            SimulationState, "/simulation/state", self.on_state, latched_qos
        )
        target_qos = QoSProfile(
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
        )
        self.create_subscription(
            HarvestTarget, TARGET_TOPIC, self.on_target, target_qos
        )
        perception_status_qos = QoSProfile(
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
        )
        self.create_subscription(
            HarvestPerceptionStatus,
            PERCEPTION_STATUS_TOPIC,
            self.on_perception_status,
            perception_status_qos,
        )
        self.snapshot_retry_timer = self.create_timer(0.5, self._retry_snapshot)
        # 최초 후보 하나가 periodic timer 직전에 들어오면 나머지 후보보다 먼저
        # 실행되는 race가 생긴다. 신규 target ID가 들어올 때마다 one-shot처럼
        # deadline을 다시 시작해 마지막 신규 ID 이후에 전체 대기열을 dispatch한다.
        self.queue_dispatch_timer = self.create_timer(
            TARGET_BATCH_DEBOUNCE_SEC,
            self._dispatch_pending_targets,
        )
        self.queue_dispatch_timer.cancel()

    @staticmethod
    def _optional_threshold(value):
        value = float(value)
        if not math.isfinite(value) or value < 0.0:
            return None
        return value

    @staticmethod
    def _stamp_ns(stamp):
        return int(stamp.sec) * 1_000_000_000 + int(stamp.nanosec)

    @staticmethod
    def _point_is_finite(point):
        return bool(
            np.all(
                np.isfinite(
                    [float(point.x), float(point.y), float(point.z)]
                )
            )
        )

    def _validate_target(self, message):
        """Validate the v2 HarvestTarget contract before planning starts."""
        if message.header.frame_id != "world":
            return "HarvestTarget header.frame_id는 world여야 합니다."
        if not str(message.target_id).strip():
            return "HarvestTarget target_id가 비어 있습니다."
        stamp_ns = self._stamp_ns(message.header.stamp)
        source_stamp_ns = self._stamp_ns(message.source_point.header.stamp)
        if stamp_ns <= 0:
            return "HarvestTarget header timestamp가 유효하지 않습니다."
        if source_stamp_ns != stamp_ns:
            return "source_point와 target의 timestamp가 일치하지 않습니다."
        if not str(message.source_point.header.frame_id).strip():
            return "source_point 원본 camera frame이 비어 있습니다."
        if message.source_point.header.frame_id == "world":
            return "source_point는 원본 camera frame이어야 합니다."
        if not self._point_is_finite(message.position):
            return "HarvestTarget world position에 NaN 또는 Inf가 있습니다."
        if not self._point_is_finite(message.source_point.point):
            return "HarvestTarget source_point에 NaN 또는 Inf가 있습니다."
        values = (
            float(message.confidence),
            float(message.valid_depth_ratio),
            float(message.tf_time_error_sec),
        )
        if not all(math.isfinite(value) for value in values):
            return "HarvestTarget 품질 메타데이터에 NaN 또는 Inf가 있습니다."
        confidence, valid_depth_ratio, tf_time_error_sec = values
        if not 0.0 <= confidence <= 1.0:
            return "confidence는 0.0~1.0 범위여야 합니다."
        if not 0.0 <= valid_depth_ratio <= 1.0:
            return "valid_depth_ratio는 0.0~1.0 범위여야 합니다."
        if tf_time_error_sec < 0.0:
            return "tf_time_error_sec는 0 이상이어야 합니다."
        if (
            self.minimum_target_confidence is not None
            and confidence < self.minimum_target_confidence
        ):
            return "target confidence threshold 미달입니다."
        if (
            self.minimum_valid_depth_ratio is not None
            and valid_depth_ratio < self.minimum_valid_depth_ratio
        ):
            return "valid depth ratio threshold 미달입니다."
        if (
            self.maximum_tf_time_error_sec is not None
            and tf_time_error_sec > self.maximum_tf_time_error_sec
        ):
            return "TF timestamp error threshold 초과입니다."
        if self.target_max_age_sec is not None:
            age_sec = (
                self.get_clock().now().nanoseconds - stamp_ns
            ) / 1_000_000_000.0
            if age_sec > self.target_max_age_sec:
                return (
                    "target timestamp가 stale합니다: "
                    f"age={age_sec:.3f}s, limit={self.target_max_age_sec:.3f}s"
                )
        return None

    def _reject_target(self, message, reason, error_code="309:INVALID_TARGET_POSE"):
        self.samples.clear()
        self._sample_target_key = None
        self._publish_status("TARGET_RECEIVED", False, 0.0, error_code, reason)
        self.get_logger().warning(
            f"HarvestTarget 거부 target_id={message.target_id}: {reason}"
        )

    def on_perception_status(self, message):
        if message.status == HarvestPerceptionStatus.OK:
            self.get_logger().debug(
                f"perception OK target_id={message.target_id}"
            )
            return
        self.get_logger().warning(
            "perception status: "
            f"status={message.status}, target_id={message.target_id}, "
            f"reset={message.reset_id}/{message.scene_version}, "
            f"message={message.message}"
        )

    def _retry_snapshot(self):
        if self.simulation_state is None or self.simulation_state.state not in (
            SimulationState.READY,
            SimulationState.PLAYING,
        ):
            return
        if self.planning_scene is None or (
            self.planning_scene.reset_id != self.simulation_state.reset_id
            or self.planning_scene.scene_version != self.simulation_state.scene_version
        ):
            self.request_snapshot()
            return
        if self.execute_enabled:
            self._tcp_pose_available()

    def _publish_status(self, state, success, progress, error_code="", message=""):
        value = MotionStatus()
        value.header.stamp = self.get_clock().now().to_msg()
        value.header.frame_id = "world"
        value.current_state = str(state)
        value.success = bool(success)
        value.progress = float(np.clip(progress, 0.0, 1.0))
        value.error_code = str(error_code)
        value.message = str(message)
        self.status_publisher.publish(value)

    @staticmethod
    def _planning_error_code(error):
        text = str(error).lower()
        if "scene" in text or "simulation" in text or "version" in text:
            return "308:SIMULATION_RESET"
        if "collision" in text or "충돌" in text:
            return "302:COLLISION_RISK"
        if "ik" in text:
            return "300:IK_FAILED"
        if "singular" in text:
            return "303:SINGULARITY_RISK"
        if "tf" in text:
            return "310:TF_UNAVAILABLE"
        return "301:APPROACH_UNREACHABLE"

    @staticmethod
    def _normalize_error_code(code):
        """Action Server의 legacy 심볼을 공통 300번대 코드로 맞춘다."""
        code = str(code or "")
        if ":" in code:
            return code
        mapping = {
            "CANCELED": "307:CANCELLED",
            "CANCELLED": "307:CANCELLED",
            "SCENE_MISMATCH": "308:SIMULATION_RESET",
            "SIMULATION_STOPPED": "308:SIMULATION_RESET",
            "INVALID_TARGET_POSE": "309:INVALID_TARGET_POSE",
            "INVALID_FRAME": "309:INVALID_TARGET_POSE",
            "INITIAL_COLLISION": "302:COLLISION_RISK",
            "UNEXPECTED_CONTACT": "302:COLLISION_RISK",
            "APPROACH_UNREACHABLE": "301:APPROACH_UNREACHABLE",
            "STEM_NOT_BROKEN": "305:STEM_NOT_BROKEN",
            "GOAL_REJECTED": "306:GOAL_REJECTED",
        }
        return mapping.get(code, "312:INTERNAL_ERROR")

    def _clear_run(self, remember_target=False):
        if remember_target and self.target is not None:
            self.failed_target = self._xyz(self.target.pose.position)
        self.running = False
        self.goal_handle = None
        self._active_target_key = None
        self.target = None
        self._active_candidate = None
        self.approach_orientation = None
        self.samples.clear()
        self._sample_target_key = None

    def _report_plan_failure(self, center, error):
        code = self._planning_error_code(error)
        if code != "308:SIMULATION_RESET":
            self.failed_target = np.asarray(center, dtype=float)
        self._publish_status("PRE_GRASP_PLANNING", False, 0.0, code, str(error))
        self.get_logger().warning(f"APPROACH 계획 실패 {code}: {error}")

    @staticmethod
    def _matrix_from_quaternion_xyzw(x, y, z, w):
        q = np.array([x, y, z, w], dtype=float)
        norm = float(np.linalg.norm(q))
        if not np.isfinite(norm) or norm <= 1e-12:
            raise RoutePlanningError("quaternion이 유효하지 않습니다.")
        x, y, z, w = q / norm
        return np.array(
            [
                [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
            ],
            dtype=float,
        )

    @staticmethod
    def _quaternion_xyzw_from_matrix(matrix):
        matrix = np.asarray(matrix, dtype=float)
        trace = float(np.trace(matrix))
        if trace > 0.0:
            scale = np.sqrt(trace + 1.0) * 2.0
            q = np.array(
                [
                    (matrix[2, 1] - matrix[1, 2]) / scale,
                    (matrix[0, 2] - matrix[2, 0]) / scale,
                    (matrix[1, 0] - matrix[0, 1]) / scale,
                    0.25 * scale,
                ]
            )
        else:
            index = int(np.argmax(np.diag(matrix)))
            if index == 0:
                scale = np.sqrt(1.0 + matrix[0, 0] - matrix[1, 1] - matrix[2, 2]) * 2.0
                q = np.array(
                    [
                        0.25 * scale,
                        (matrix[0, 1] + matrix[1, 0]) / scale,
                        (matrix[0, 2] + matrix[2, 0]) / scale,
                        (matrix[2, 1] - matrix[1, 2]) / scale,
                    ]
                )
            elif index == 1:
                scale = np.sqrt(1.0 + matrix[1, 1] - matrix[0, 0] - matrix[2, 2]) * 2.0
                q = np.array(
                    [
                        (matrix[0, 1] + matrix[1, 0]) / scale,
                        0.25 * scale,
                        (matrix[1, 2] + matrix[2, 1]) / scale,
                        (matrix[0, 2] - matrix[2, 0]) / scale,
                    ]
                )
            else:
                scale = np.sqrt(1.0 + matrix[2, 2] - matrix[0, 0] - matrix[1, 1]) * 2.0
                q = np.array(
                    [
                        (matrix[0, 2] + matrix[2, 0]) / scale,
                        (matrix[1, 2] + matrix[2, 1]) / scale,
                        0.25 * scale,
                        (matrix[1, 0] - matrix[0, 1]) / scale,
                    ]
                )
        return q / np.linalg.norm(q)

    def _lookup_tcp_frame(self, stamp):
        """Return the world-to-palm transform as rotation and position."""
        try:
            transform = self.tf_buffer.lookup_transform(
                "world", TCP_FRAME, stamp
            )
        except TransformException as error:
            raise RoutePlanningError(
                f"{TCP_FRAME} TF is unavailable: {error}"
            )
        rotation = self._matrix_from_quaternion_xyzw(
            transform.transform.rotation.x,
            transform.transform.rotation.y,
            transform.transform.rotation.z,
            transform.transform.rotation.w,
        )
        position = np.array(
            [
                transform.transform.translation.x,
                transform.transform.translation.y,
                transform.transform.translation.z,
            ],
            dtype=float,
        )
        return rotation, position

    def _report_tcp_lookup_failure(self, message):
        """Report a changed TCP lookup failure with the live TF tree."""
        try:
            frames = self.tf_buffer.all_frames_as_string()
        except Exception as error:
            frames = f"Unable to read TF tree: {error}"
        failure = f"{message}\nCurrent TF tree:\n{frames}"
        if failure == self._last_tcp_lookup_failure:
            return
        self._last_tcp_lookup_failure = failure
        self.get_logger().warning(failure)

    def _tcp_pose_available(self):
        try:
            self._lookup_tcp_frame(Time())
        except RoutePlanningError as error:
            self._report_tcp_lookup_failure(str(error))
            return False
        self._last_tcp_lookup_failure = None
        return True

    def _current_tcp_pose(self):
        """Read the current world-to-palm TF and apply the palm-local TCP offset."""
        palm_rotation, palm_position = self._lookup_tcp_frame(Time())
        tcp_position = palm_position + palm_rotation @ np.array(
            [0.0, PALM_TO_TCP_Y_M, 0.0],
            dtype=float,
        )
        quaternion = self._quaternion_xyzw_from_matrix(palm_rotation)
        value = PoseStamped()
        value.header.stamp = self.get_clock().now().to_msg()
        value.header.frame_id = "world"
        value.pose.position.x = float(tcp_position[0])
        value.pose.position.y = float(tcp_position[1])
        value.pose.position.z = float(tcp_position[2])
        value.pose.orientation.x = float(quaternion[0])
        value.pose.orientation.y = float(quaternion[1])
        value.pose.orientation.z = float(quaternion[2])
        value.pose.orientation.w = float(quaternion[3])
        return value

    def on_state(self, message):
        previous = self.simulation_state
        self.simulation_state = message
        if previous is None or (
            previous.state != message.state
            or previous.reset_id != message.reset_id
            or previous.scene_version != message.scene_version
        ):
            self.get_logger().info(
                f"simulation state={message.state}, reset={message.reset_id}, "
                f"scene={message.scene_version}: {message.message}"
            )
        version_changed = previous is not None and (
            previous.reset_id != message.reset_id
            or previous.scene_version != message.scene_version
        )
        reset_changed = previous is not None and (
            previous.reset_id != message.reset_id
        )
        if reset_changed and self.safety_stopped:
            self.safety_stopped = False
            self.safety_stop_reason = None
            self.get_logger().info(
                "reset_id 변경으로 연속 수확 SAFETY_STOPPED 상태를 해제합니다."
            )
        invalidating = message.state in (
            SimulationState.STOPPED,
            SimulationState.INITIALIZING,
        )
        if version_changed or invalidating:
            self.queue_dispatch_timer.cancel()
            self.generation += 1
            if self.running and self.goal_handle is not None:
                self.get_logger().warning(
                    "Stop/Reset 또는 scene 변경을 감지해 실행 중 Goal을 취소합니다."
                )
                self.goal_handle.cancel_goal_async()
            self.running = False
            self.goal_handle = None
            self.target = None
            self.approach_orientation = None
            self.samples.clear()
            self.target_samples.clear()
            self.pending_targets.clear()
            self.retry_targets.clear()
            self._sample_target_key = None
            self._active_target_key = None
            self._active_candidate = None
            if version_changed:
                self.failed_target = None
                self.planning_scene = None
                self._latest_target_stamps.clear()
                if previous.reset_id != message.reset_id:
                    self._started_target_keys.clear()
                    self.completed_target_keys.clear()
                    self.failed_once_target_keys.clear()
                    self.final_failed_target_keys.clear()
        if message.state in (SimulationState.READY, SimulationState.PLAYING):
            if (
                self.planning_scene is None
                or self.planning_scene.reset_id != message.reset_id
                or self.planning_scene.scene_version != message.scene_version
            ):
                self.request_snapshot()

    def on_scene(self, message):
        if message.header.frame_id != "world":
            self.get_logger().error("planning scene frame_id가 world가 아닙니다.")
            return
        if not message.obstacles:
            self.get_logger().error("planning scene obstacle 목록이 비어 있습니다.")
            return
        if self.simulation_state is not None and (
            message.reset_id != self.simulation_state.reset_id
            or message.scene_version != self.simulation_state.scene_version
        ):
            self.get_logger().warning(
                "simulation state와 버전이 다른 planning scene을 폐기합니다."
            )
            return
        self.planning_scene = message
        self.snapshot_request_pending = False
        self.get_logger().info(
            f"planning scene 동기화: reset={message.reset_id}, "
            f"version={message.scene_version}, obstacles={len(message.obstacles)}"
        )

    def request_snapshot(self):
        if self.snapshot_request_pending or not self.scene_client.service_is_ready():
            return
        self.snapshot_request_pending = True
        future = self.scene_client.call_async(GetPlanningScene.Request())
        future.add_done_callback(self.on_snapshot_response)

    def on_snapshot_response(self, future):
        self.snapshot_request_pending = False
        try:
            response = future.result()
        except Exception as error:
            self.get_logger().warning(f"planning scene 재요청 실패: {error}")
            return
        if response.success:
            self.on_scene(response.scene)
        else:
            self.get_logger().warning(response.message)

    @staticmethod
    def _xyz(position):
        return np.array([position.x, position.y, position.z], dtype=float)

    def _planning_inputs_synchronized(self):
        state = self.simulation_state
        if state is None or state.state not in (
            SimulationState.READY,
            SimulationState.PLAYING,
        ):
            return False
        scene = self.planning_scene
        if scene is None:
            self.request_snapshot()
            return False
        if (
            scene.reset_id != state.reset_id
            or scene.scene_version != state.scene_version
        ):
            self.planning_scene = None
            self.request_snapshot()
            return False
        if self.execute_enabled and not self._tcp_pose_available():
            return False
        return True

    def _prepare_approach_goal(self, center):
        """현재 scene 세대를 고정하고 GPU PC 1의 기본 접근 자세를 계산한다.

        실제 c-space 경로 생성과 collision 재검증은 같은 GPU PC 1에서 실행되는
        RobotMotion Action 서버가 담당한다. 이 coordinator는 외부 waypoint를
        만들어 Action Goal에 주입하지 않는다.
        """
        if self.simulation_state is None or self.simulation_state.state not in (
            SimulationState.READY,
            SimulationState.PLAYING,
        ):
            raise RoutePlanningError("GPU PC 1 simulation이 READY/PLAYING 상태가 아닙니다.")
        scene = self.planning_scene
        if scene is None:
            self.request_snapshot()
            raise RoutePlanningError("planning scene snapshot을 아직 받지 못했습니다.")
        try:
            validate_scene_version(
                scene.reset_id,
                scene.scene_version,
                self.simulation_state.reset_id,
                self.simulation_state.scene_version,
            )
        except RoutePlanningError:
            self.planning_scene = None
            self.request_snapshot()
            raise RoutePlanningError("planning scene 버전이 현재 simulation과 다릅니다.")
        robot_base = self._xyz(scene.robot_base_pose.pose.position)
        approach_orientation = approach_orientation_xyzw(robot_base, center)
        self.get_logger().info(
            "APPROACH target 승인: GPU PC 1 Action 서버가 현재 관절 상태와 "
            f"scene {scene.reset_id}/{scene.scene_version}으로 경로를 생성합니다."
        )
        return (
            scene.reset_id,
            scene.scene_version,
            approach_orientation,
        )

    def _candidate_distance_from_robot(self, candidate):
        if self.planning_scene is None:
            return float("inf")
        robot_base = self._xyz(
            self.planning_scene.robot_base_pose.pose.position
        )
        return float(np.linalg.norm(candidate.center - robot_base))

    def _defer_or_finish_failed_candidate(self, candidate, reason):
        """접촉 전 첫 실패만 후순위 큐로 보내고 두 번째 실패는 종료한다."""
        if candidate is None:
            return
        key = candidate.key
        if key not in self.failed_once_target_keys:
            self.failed_once_target_keys.add(key)
            self.retry_targets[key] = candidate
            self.get_logger().warning(
                f"target_id={key[1]} 첫 실패; 다른 사과 처리 후 1회 재시도: "
                f"{reason}"
            )
            return
        self.retry_targets.pop(key, None)
        self.final_failed_target_keys.add(key)
        self.get_logger().error(
            f"target_id={key[1]} 재시도 실패; 최종 실패 처리: {reason}"
        )

    def _handle_active_failure(
        self,
        reason,
        allow_deferred_retry,
        error_code="301:APPROACH_UNREACHABLE",
    ):
        candidate = self._active_candidate
        self._clear_run(remember_target=True)
        # APPROACH 단계라는 이유만으로 실제 접촉까지 planning 실패로 재시도하면
        # 접촉 자세에서 다음 사과의 RRT가 시작된다. 301의 순수 접근 불가만
        # 후순위로 보내고 302는 접촉 이후 실패로 안전 정지한다.
        normalized_error = self._normalize_error_code(error_code)
        if allow_deferred_retry and normalized_error == "301:APPROACH_UNREACHABLE":
            self._defer_or_finish_failed_candidate(candidate, reason)
            self._start_next_target()
            return
        if candidate is not None:
            self.final_failed_target_keys.add(candidate.key)
        self.safety_stopped = True
        self.safety_stop_reason = str(reason)
        self.pending_targets.clear()
        self.retry_targets.clear()
        self.queue_dispatch_timer.cancel()
        self._publish_status(
            "SAFETY_STOPPED",
            False,
            0.0,
            "302:COLLISION_RISK",
            "접촉 이후 실패로 reset 전까지 연속 수확을 중단합니다: "
            f"{reason}",
        )
        self.get_logger().error(
            "접촉 이후 실패로 SAFETY_STOPPED 상태에 진입했습니다. "
            "reset_id가 변경될 때까지 다음 target을 실행하지 않습니다: "
            f"{reason}"
        )

    def _start_next_target(self):
        """일반 대기열을 모두 처리한 뒤 후순위 재시도 대기열을 실행한다."""
        self.queue_dispatch_timer.cancel()
        if self.running or self.safety_stopped:
            return
        while self.pending_targets or self.retry_targets:
            queue = self.pending_targets if self.pending_targets else self.retry_targets
            candidate = min(
                queue.values(),
                key=self._candidate_distance_from_robot,
            )
            queue.pop(candidate.key, None)
            try:
                reset_id, scene_version, approach_orientation = (
                    self._prepare_approach_goal(candidate.center)
                )
            except (RoutePlanningError, ValueError) as error:
                self._report_plan_failure(candidate.center, error)
                self._defer_or_finish_failed_candidate(candidate, error)
                continue

            if not self.execute_enabled:
                self._publish_status(
                    "PRE_GRASP_PLANNING",
                    True,
                    1.0,
                    "",
                    f"target_id={candidate.key[1]} target·scene·접근 자세 검증 완료; "
                    "경로 실행은 비활성화됨",
                )
                self.completed_target_keys.add(candidate.key)
                continue

            self.target = PoseStamped()
            self.target.header = candidate.message.header
            self.target.pose.position.x = float(candidate.center[0])
            self.target.pose.position.y = float(candidate.center[1])
            self.target.pose.position.z = float(candidate.center[2])
            if approach_orientation is None:
                self.target.pose.orientation.w = 1.0
            else:
                self.target.pose.orientation.x = float(approach_orientation[0])
                self.target.pose.orientation.y = float(approach_orientation[1])
                self.target.pose.orientation.z = float(approach_orientation[2])
                self.target.pose.orientation.w = float(approach_orientation[3])
            self.failed_target = None
            self.plan_reset_id = int(reset_id)
            self.plan_scene_version = int(scene_version)
            self.approach_orientation = approach_orientation
            self._active_target_key = candidate.key
            self._active_candidate = candidate
            self.running, self.index = True, 0
            self.get_logger().info(
                f"연속 수확 시작 target_id={candidate.key[1]}, "
                f"pending={len(self.pending_targets)}, retry={len(self.retry_targets)}"
            )
            self.send_next()
            return

    def _dispatch_pending_targets(self):
        """마지막 신규 target ID 이후 모인 전체 후보를 한 번만 dispatch한다."""
        self.queue_dispatch_timer.cancel()
        self._start_next_target()

    def on_target(self, message):
        """Receive and validate the v2 HarvestTarget contract."""
        validation_error = self._validate_target(message)
        if validation_error is not None:
            self._reject_target(message, validation_error)
            return
        if self.safety_stopped:
            self._reject_target(
                message,
                "접촉 이후 실패로 SAFETY_STOPPED 상태입니다. "
                "Timeline reset 후 다시 시도해야 합니다."
                + (
                    ""
                    if not self.safety_stop_reason
                    else f" 원인: {self.safety_stop_reason}"
                ),
                "302:COLLISION_RISK",
            )
            return

        state = self.simulation_state
        if state is None or state.state not in (
            SimulationState.READY,
            SimulationState.PLAYING,
        ):
            self._reject_target(
                message,
                "SimulationState가 READY 또는 PLAYING이 아닙니다.",
                "306:GOAL_REJECTED",
            )
            return
        if (
            int(message.reset_id) != int(state.reset_id)
            or int(message.scene_version) != int(state.scene_version)
        ):
            self._reject_target(
                message,
                "target reset_id/scene_version이 현재 SimulationState와 다릅니다.",
                "308:SIMULATION_RESET",
            )
            return
        if not self._planning_inputs_synchronized():
            self._reject_target(
                message,
                "planning scene 또는 현재 TCP가 아직 동기화되지 않았습니다.",
                "306:GOAL_REJECTED",
            )
            return

        target_key = (int(message.reset_id), str(message.target_id))
        if (
            target_key in self._started_target_keys
            or target_key in self.completed_target_keys
            or target_key in self.failed_once_target_keys
            or target_key in self.final_failed_target_keys
            or target_key == self._active_target_key
        ):
            self.get_logger().debug(
                "이미 시작·완료·최종 실패한 HarvestTarget 갱신 무시: "
                f"target_id={message.target_id}, reset_id={message.reset_id}"
            )
            return
        stamp_ns = self._stamp_ns(message.header.stamp)
        previous_stamp_ns = self._latest_target_stamps.get(target_key)
        if previous_stamp_ns is not None and stamp_ns <= previous_stamp_ns:
            self.get_logger().debug(
                "오래된 HarvestTarget 무시: "
                f"target_id={message.target_id}, stamp={stamp_ns}, "
                f"latest={previous_stamp_ns}"
            )
            return
        self._latest_target_stamps[target_key] = stamp_ns

        sample = self._xyz(message.position)
        samples = self.target_samples.get(target_key)
        if samples is None:
            samples = deque(maxlen=self.sample_count)
            self.target_samples[target_key] = samples
        samples.append(sample)
        if len(samples) < samples.maxlen:
            return
        values = np.asarray(samples)
        center = np.median(values, axis=0)
        spread = float(np.max(np.linalg.norm(values - center, axis=1)))
        self.get_logger().info(
            f"target_id={message.target_id} median={center}, "
            f"spread={spread:.4f} m"
        )
        if spread > self.maximum_spread:
            return
        is_new_candidate = target_key not in self.pending_targets
        candidate = PendingTarget(
            key=target_key,
            message=message,
            center=np.asarray(center, dtype=float).copy(),
            stamp_ns=stamp_ns,
        )
        self.pending_targets[target_key] = candidate
        self.get_logger().info(
            f"target_id={message.target_id} 연속 수확 대기열 등록; "
            f"pending={len(self.pending_targets)}"
        )
        if is_new_candidate and not self.running and not self.safety_stopped:
            self.queue_dispatch_timer.reset()

    def send_next(self):
        if self.index >= len(SEQUENCE):
            completed_key = self._active_target_key
            if completed_key is not None:
                self.completed_target_keys.add(completed_key)
                self.retry_targets.pop(completed_key, None)
            self.get_logger().info(
                "수확 Action 시퀀스 완료"
                + (
                    ""
                    if completed_key is None
                    else f" target_id={completed_key[1]}"
                )
            )
            self._clear_run(remember_target=False)
            self._start_next_target()
            return
        generation = self.generation
        motion_type = SEQUENCE[self.index]
        if motion_type in (RobotMotion.Goal.GRASP, RobotMotion.Goal.RELEASE):
            try:
                target_pose = self._current_tcp_pose()
            except RoutePlanningError as error:
                self._report_plan_failure(self._xyz(self.target.pose.position), error)
                self._handle_active_failure(
                    error,
                    allow_deferred_retry=(self.index == 0),
                )
                return
        else:
            target_pose = self.target
        if not self.client.wait_for_server(timeout_sec=2.0):
            self.get_logger().error("/harvest/robot_motion 서버를 찾을 수 없습니다.")
            self._publish_status(
                "ACTION_WAIT", False, 0.0, "306:GOAL_REJECTED", "RobotMotion 서버를 찾을 수 없습니다."
            )
            self._handle_active_failure(
                "RobotMotion 서버를 찾을 수 없습니다.",
                allow_deferred_retry=(self.index == 0),
            )
            return
        goal = RobotMotion.Goal()
        goal.motion_type = motion_type
        goal.target_pose = target_pose
        goal.reset_id = self.plan_reset_id
        goal.scene_version = self.plan_scene_version
        future = self.client.send_goal_async(goal, feedback_callback=self.on_feedback)
        future.add_done_callback(
            lambda result_future: self.on_goal_response(result_future, generation)
        )

    def on_goal_response(self, future, generation):
        try:
            handle = future.result()
        except Exception as error:
            self._publish_status("ACTION_WAIT", False, 0.0, "312:INTERNAL_ERROR", str(error))
            self._handle_active_failure(
                error,
                allow_deferred_retry=(self.index == 0),
            )
            return
        if generation != self.generation or not self.running:
            if handle.accepted:
                handle.cancel_goal_async()
            return
        if not handle.accepted:
            self._publish_status(
                "GOAL_REJECTED",
                False,
                0.0,
                "306:GOAL_REJECTED",
                "simulation/scene 버전 또는 Action 상태로 Goal이 거부되었습니다.",
            )
            self._handle_active_failure(
                "RobotMotion Goal이 거부되었습니다.",
                allow_deferred_retry=(self.index == 0),
            )
            return
        if self.index == 0 and self._active_target_key is not None:
            self._started_target_keys.add(self._active_target_key)
        self.goal_handle = handle
        handle.get_result_async().add_done_callback(
            lambda result_future: self.on_result(result_future, generation)
        )

    def on_feedback(self, message):
        feedback = message.feedback
        self.get_logger().info(
            f"{feedback.current_state}: {100.0 * feedback.progress:.0f}%"
        )

    def on_result(self, future, generation):
        if generation != self.generation or not self.running:
            return
        self.goal_handle = None
        try:
            result = future.result().result
        except Exception as error:
            self._publish_status("ACTION_RESULT", False, 0.0, "312:INTERNAL_ERROR", str(error))
            self._handle_active_failure(
                error,
                allow_deferred_retry=(self.index == 0),
            )
            return
        if not result.success:
            self.get_logger().error(f"{result.error_code}: {result.message}")
            error_code = self._normalize_error_code(result.error_code)
            self._publish_status(
                "ACTION_RESULT", False, 0.0, error_code, result.message
            )
            self._handle_active_failure(
                result.message,
                allow_deferred_retry=(self.index == 0),
                error_code=error_code,
            )
            return
        self.index += 1
        self.send_next()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="없으면 좌표만 검증")
    parser.add_argument("--samples", type=int, default=10)
    parser.add_argument("--maximum-spread", type=float, default=0.04)
    args, ros_args = parser.parse_known_args()
    rclpy.init(args=ros_args)
    node = HarvestCoordinator(args.execute, args.samples, args.maximum_spread)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
