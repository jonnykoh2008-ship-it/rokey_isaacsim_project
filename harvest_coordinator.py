"""개인 PC 1용 분산 충돌 계획 상태 머신 및 RobotMotion Action Client."""

import argparse
from collections import deque

import numpy as np
import rclpy
from appleproj_interfaces.action import RobotMotion
from appleproj_interfaces.msg import PlanningScene, SimulationState
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


SEQUENCE = [
    RobotMotion.Goal.APPROACH,
    RobotMotion.Goal.GRASP,
    RobotMotion.Goal.TWIST,
    RobotMotion.Goal.PULL,
    RobotMotion.Goal.TRANSPORT,
    RobotMotion.Goal.PLACE,
    RobotMotion.Goal.RETRACT,
]


class HarvestCoordinator(Node):
    def __init__(self, execute, sample_count, maximum_spread):
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
        self.snapshot_request_pending = False

        latched_qos = QoSProfile(
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
        )
        self.client = ActionClient(self, RobotMotion, "/harvest/robot_motion")
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
            if self.running and self.goal_handle is not None:
                self.get_logger().warning(
                    "Stop/Reset 또는 scene 변경을 감지해 실행 중 Goal을 취소합니다."
                )
                self.goal_handle.cancel_goal_async()
            self.running = False
            self.goal_handle = None
            self.target = None
            self.approach_waypoints = []
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
        )

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
        start_tcp = self._xyz(scene.robot_tcp_pose.pose.position)
        robot_base = self._xyz(scene.robot_base_pose.pose.position)
        proxies = [self._proxy_from_message(value) for value in scene.obstacles]
        route = plan_approach_route(start_tcp, robot_base, center, proxies)
        waypoints = []
        q = route.orientation_xyzw
        for position in route.positions:
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
            f"clearance={route.minimum_clearance:.3f} m, "
            f"closest={route.closest_obstacle}"
        )
        return scene.reset_id, scene.scene_version, waypoints

    def on_pose(self, message):
        if message.header.frame_id != "world" or self.running:
            return
        sample = self._xyz(message.pose.position)
        if not np.all(np.isfinite(sample)):
            return
        self.samples.append(sample)
        if len(self.samples) < self.samples.maxlen:
            return
        values = np.asarray(self.samples)
        center = np.median(values, axis=0)
        spread = float(np.max(np.linalg.norm(values - center, axis=1)))
        self.get_logger().info(f"target median={center}, spread={spread:.4f} m")
        if spread > self.maximum_spread or not self.execute_enabled:
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
            reset_id, scene_version, waypoints = self._prepare_approach_plan(
                center, message.header
            )
        except (RoutePlanningError, ValueError) as error:
            self.get_logger().warning(f"APPROACH 계획 보류: {error}")
            self.samples.clear()
            return
        self.target = PoseStamped()
        self.target.header = message.header
        self.target.pose.position.x = float(center[0])
        self.target.pose.position.y = float(center[1])
        self.target.pose.position.z = float(center[2])
        self.target.pose.orientation.w = 1.0
        self.failed_target = None
        self.samples.clear()
        self.plan_reset_id = int(reset_id)
        self.plan_scene_version = int(scene_version)
        self.approach_waypoints = waypoints
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
        if not self.client.wait_for_server(timeout_sec=2.0):
            self.get_logger().error("/harvest/robot_motion 서버를 찾을 수 없습니다.")
            self.running = False
            return
        goal = RobotMotion.Goal()
        goal.motion_type = SEQUENCE[self.index]
        goal.target_pose = self.target
        goal.reset_id = self.plan_reset_id
        goal.scene_version = self.plan_scene_version
        if goal.motion_type == RobotMotion.Goal.APPROACH:
            goal.waypoints = self.approach_waypoints
        future = self.client.send_goal_async(goal, feedback_callback=self.on_feedback)
        future.add_done_callback(self.on_goal_response)

    def on_goal_response(self, future):
        handle = future.result()
        if not handle.accepted:
            self.get_logger().error(
                "RobotMotion Goal이 거부되었습니다. simulation/scene 버전을 확인하세요."
            )
            self.running = False
            return
        self.goal_handle = handle
        handle.get_result_async().add_done_callback(self.on_result)

    def on_feedback(self, message):
        feedback = message.feedback
        self.get_logger().info(
            f"{feedback.current_state}: {100.0 * feedback.progress:.0f}%"
        )

    def on_result(self, future):
        self.goal_handle = None
        result = future.result().result
        if not result.success:
            self.get_logger().error(f"{result.error_code}: {result.message}")
            if self.target is not None:
                self.failed_target = self._xyz(self.target.pose.position)
            self.running = False
            self.target = None
            self.approach_waypoints = []
            self.samples.clear()
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
