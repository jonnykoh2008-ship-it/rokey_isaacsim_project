"""개인 PC 1용 수확 상태 머신 및 RobotMotion Action Client."""

import argparse
from collections import deque

import numpy as np
import rclpy
from appleproj_interfaces.action import RobotMotion
from geometry_msgs.msg import PoseStamped
from rclpy.action import ActionClient
from rclpy.node import Node


SEQUENCE = [
    RobotMotion.Goal.APPROACH, RobotMotion.Goal.GRASP, RobotMotion.Goal.TWIST,
    RobotMotion.Goal.PULL, RobotMotion.Goal.TRANSPORT, RobotMotion.Goal.PLACE,
    RobotMotion.Goal.RETRACT,
]


class HarvestCoordinator(Node):
    def __init__(self, execute, sample_count, maximum_spread):
        super().__init__("harvest_coordinator")
        self.execute_enabled = execute
        self.samples = deque(maxlen=sample_count)
        self.maximum_spread = maximum_spread
        self.target = None
        self.index = 0
        self.running = False
        self.client = ActionClient(self, RobotMotion, "/harvest/robot_motion")
        self.create_subscription(PoseStamped, "/harvest/target_pose", self.on_pose, 10)

    def on_pose(self, message):
        if message.header.frame_id != "world" or self.running:
            return
        p = message.pose.position
        sample = np.array([p.x, p.y, p.z], dtype=float)
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
        self.target = PoseStamped()
        self.target.header = message.header
        self.target.pose.position.x, self.target.pose.position.y, self.target.pose.position.z = center
        self.target.pose.orientation.w = 1.0
        self.running, self.index = True, 0
        self.send_next()

    def send_next(self):
        if self.index >= len(SEQUENCE):
            self.get_logger().info("수확 Action 시퀀스 완료")
            return
        if not self.client.wait_for_server(timeout_sec=2.0):
            self.get_logger().error("/harvest/robot_motion 서버를 찾을 수 없습니다.")
            self.running = False
            return
        goal = RobotMotion.Goal()
        goal.motion_type, goal.target_pose = SEQUENCE[self.index], self.target
        future = self.client.send_goal_async(goal, feedback_callback=self.on_feedback)
        future.add_done_callback(self.on_goal_response)

    def on_goal_response(self, future):
        handle = future.result()
        if not handle.accepted:
            self.get_logger().error("RobotMotion Goal이 거부되었습니다.")
            self.running = False
            return
        handle.get_result_async().add_done_callback(self.on_result)

    def on_feedback(self, message):
        f = message.feedback
        self.get_logger().info(f"{f.current_state}: {100.0 * f.progress:.0f}%")

    def on_result(self, future):
        result = future.result().result
        if not result.success:
            self.get_logger().error(f"{result.error_code}: {result.message}")
            self.running = False
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
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
