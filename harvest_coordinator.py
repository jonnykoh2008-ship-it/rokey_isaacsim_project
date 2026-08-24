"""개인 PC 1용 분산 충돌 계획 상태 머신 및 RobotMotion Action Client."""

import argparse
from collections import deque

import numpy as np
import rclpy
from appleproj_interfaces.action import RobotMotion
from appleproj_interfaces.msg import MotionStatus, PlanningScene, SimulationState
from appleproj_interfaces.srv import GetPlanningScene
from geometry_msgs.msg import PoseStamped
from harvest_route_planner import (
    Proxy,
    RoutePlanningError,
    plan_approach_route,
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
        self.samples = deque(maxlen=sample_count)
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
        self.approach_waypoints = []
        self.approach_orientation = None
        self.snapshot_request_pending = False
        self.generation = 0
        self._last_tcp_lookup_failure = None

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
        self.create_subscription(
            PoseStamped, "/harvest/target_pose", self.on_pose, 10
        )
        self.snapshot_retry_timer = self.create_timer(0.5, self._retry_snapshot)

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
        self.target = None
        self.approach_waypoints = []
        self.approach_orientation = None
        self.samples.clear()

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
        invalidating = message.state in (
            SimulationState.STOPPED,
            SimulationState.INITIALIZING,
        )
        if version_changed or invalidating:
            self.generation += 1
            if self.running and self.goal_handle is not None:
                self.get_logger().warning(
                    "Stop/Reset 또는 scene 변경을 감지해 실행 중 Goal을 취소합니다."
                )
                self.goal_handle.cancel_goal_async()
            self.running = False
            self.goal_handle = None
            self.target = None
            self.approach_waypoints = []
            self.approach_orientation = None
            self.samples.clear()
            if version_changed:
                self.failed_target = None
                self.planning_scene = None
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

    @staticmethod
    def _proxy_from_message(message):
        orientation = message.pose.orientation
        return Proxy(
            obstacle_id=message.obstacle_id,
            shape=int(message.shape),
            position=HarvestCoordinator._xyz(message.pose.position),
            orientation_xyzw=np.array(
                [orientation.x, orientation.y, orientation.z, orientation.w],
                dtype=float,
            ),
            dimensions=np.array(
                [message.dimensions.x, message.dimensions.y, message.dimensions.z],
                dtype=float,
            ),
            safety_margin=float(message.safety_margin),
            obstacle_class=int(message.obstacle_class),
        )

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

    def _prepare_approach_plan(self, center, target_header):
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
        planning_start = (
            self._current_tcp_pose()
            if self.execute_enabled
            else scene.robot_tcp_pose
        )
        start_tcp = self._xyz(planning_start.pose.position)
        start_orientation = np.array(
            [
                planning_start.pose.orientation.x,
                planning_start.pose.orientation.y,
                planning_start.pose.orientation.z,
                planning_start.pose.orientation.w,
            ],
            dtype=float,
        )
        robot_base = self._xyz(scene.robot_base_pose.pose.position)
        proxies = [self._proxy_from_message(value) for value in scene.obstacles]
        route = plan_approach_route(
            start_tcp,
            robot_base,
            center,
            proxies,
            start_orientation_xyzw=start_orientation,
        )
        waypoints = []
        for planned_waypoint in route.waypoints:
            position = planned_waypoint.position
            q = planned_waypoint.orientation_xyzw
            waypoint = PoseStamped()
            waypoint.header = target_header
            waypoint.header.frame_id = "world"
            waypoint.pose.position.x = float(position[0])
            waypoint.pose.position.y = float(position[1])
            waypoint.pose.position.z = float(position[2])
            waypoint.pose.orientation.x = float(q[0])
            waypoint.pose.orientation.y = float(q[1])
            waypoint.pose.orientation.z = float(q[2])
            waypoint.pose.orientation.w = float(q[3])
            waypoints.append(waypoint)
        self.get_logger().info(
            f"APPROACH plan={route.name}, waypoints={len(waypoints)}, "
            f"phases={','.join(value.phase for value in route.waypoints)}, "
            f"clearance={route.minimum_clearance:.3f} m, "
            f"closest={route.closest_obstacle}"
        )
        return (
            scene.reset_id,
            scene.scene_version,
            waypoints,
            route.final_orientation_xyzw,
        )

    def on_pose(self, message):
        if message.header.frame_id != "world" or self.running:
            return
        orientation = np.array(
            [
                message.pose.orientation.x,
                message.pose.orientation.y,
                message.pose.orientation.z,
                message.pose.orientation.w,
            ],
            dtype=float,
        )
        if not np.all(np.isfinite(orientation)) or np.linalg.norm(orientation) <= 1e-12:
            self._publish_status(
                "TARGET_RECEIVED",
                False,
                0.0,
                "309:INVALID_TARGET_POSE",
                "target_pose orientation이 유효하지 않습니다.",
            )
            return
        sample = self._xyz(message.pose.position)
        if not np.all(np.isfinite(sample)):
            return
        if not self._planning_inputs_synchronized():
            self.samples.clear()
            return
        self.samples.append(sample)
        if len(self.samples) < self.samples.maxlen:
            return
        values = np.asarray(self.samples)
        center = np.median(values, axis=0)
        spread = float(np.max(np.linalg.norm(values - center, axis=1)))
        self.get_logger().info(f"target median={center}, spread={spread:.4f} m")
        if spread > self.maximum_spread:
            return
        if (
            self.failed_target is not None
            and np.linalg.norm(center - self.failed_target) <= self.maximum_spread
        ):
            self.get_logger().warning(
                "직전 실패 사과와 같은 위치이므로 자동 재시도하지 않습니다. "
                "재시도하려면 coordinator를 다시 시작하세요."
            )
            self.samples.clear()
            return
        try:
            reset_id, scene_version, waypoints, approach_orientation = self._prepare_approach_plan(
                center, message.header
            )
        except (RoutePlanningError, ValueError) as error:
            self._report_plan_failure(center, error)
            self.samples.clear()
            return
        if not self.execute_enabled:
            self._publish_status(
                "PRE_GRASP_PLANNING",
                True,
                1.0,
                "",
                f"계획 검증 완료: waypoints={len(waypoints)}",
            )
            self.samples.clear()
            return
        self.target = PoseStamped()
        self.target.header = message.header
        self.target.pose.position.x = float(center[0])
        self.target.pose.position.y = float(center[1])
        self.target.pose.position.z = float(center[2])
        if approach_orientation is None:
            self.target.pose.orientation.w = 1.0
        else:
            self.target.pose.orientation.x = float(approach_orientation[0])
            self.target.pose.orientation.y = float(approach_orientation[1])
            self.target.pose.orientation.z = float(approach_orientation[2])
            self.target.pose.orientation.w = float(approach_orientation[3])
        self.failed_target = None
        self.samples.clear()
        self.plan_reset_id = int(reset_id)
        self.plan_scene_version = int(scene_version)
        self.approach_waypoints = waypoints
        self.approach_orientation = approach_orientation
        self.running, self.index = True, 0
        self.send_next()

    def send_next(self):
        if self.index >= len(SEQUENCE):
            self.get_logger().info("수확 Action 시퀀스 완료")
            self.running = False
            self.target = None
            self.approach_waypoints = []
            self.samples.clear()
            return
        generation = self.generation
        motion_type = SEQUENCE[self.index]
        if motion_type in (RobotMotion.Goal.GRASP, RobotMotion.Goal.RELEASE):
            try:
                target_pose = self._current_tcp_pose()
            except RoutePlanningError as error:
                self._report_plan_failure(self._xyz(self.target.pose.position), error)
                self._clear_run(remember_target=True)
                return
        else:
            target_pose = self.target
        if not self.client.wait_for_server(timeout_sec=2.0):
            self.get_logger().error("/harvest/robot_motion 서버를 찾을 수 없습니다.")
            self._publish_status(
                "ACTION_WAIT", False, 0.0, "306:GOAL_REJECTED", "RobotMotion 서버를 찾을 수 없습니다."
            )
            self._clear_run(remember_target=True)
            return
        goal = RobotMotion.Goal()
        goal.motion_type = motion_type
        goal.target_pose = target_pose
        goal.reset_id = self.plan_reset_id
        goal.scene_version = self.plan_scene_version
        if goal.motion_type == RobotMotion.Goal.APPROACH:
            goal.waypoints = self.approach_waypoints
        future = self.client.send_goal_async(goal, feedback_callback=self.on_feedback)
        future.add_done_callback(
            lambda result_future: self.on_goal_response(result_future, generation)
        )

    def on_goal_response(self, future, generation):
        try:
            handle = future.result()
        except Exception as error:
            self._publish_status("ACTION_WAIT", False, 0.0, "312:INTERNAL_ERROR", str(error))
            self._clear_run(remember_target=True)
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
            self._clear_run(remember_target=True)
            return
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
            self._clear_run(remember_target=True)
            return
        if not result.success:
            self.get_logger().error(f"{result.error_code}: {result.message}")
            error_code = self._normalize_error_code(result.error_code)
            self._publish_status(
                "ACTION_RESULT", False, 0.0, error_code, result.message
            )
            self._clear_run(remember_target=True)
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
