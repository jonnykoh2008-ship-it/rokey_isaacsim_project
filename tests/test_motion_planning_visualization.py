import unittest
from types import SimpleNamespace

import numpy as np
from builtin_interfaces.msg import Time
from geometry_msgs.msg import Pose
from nav_msgs.msg import Path
from trajectory_msgs.msg import JointTrajectory
from visualization_msgs.msg import Marker, MarkerArray

from motion_planning_visualization import MotionPlanningVisualizationPublisher


class FakePublisher:
    def __init__(self):
        self.messages = []

    def publish(self, message):
        self.messages.append(message)


class FakeLogger:
    def __init__(self):
        self.warnings = []

    def info(self, _message):
        pass

    def warning(self, message):
        self.warnings.append(message)


class FakeNode:
    def __init__(self):
        self.publishers = {}
        self.logger = FakeLogger()

    def create_publisher(self, message_type, topic, _qos):
        publisher = FakePublisher()
        self.publishers[(message_type, topic)] = publisher
        return publisher

    def get_clock(self):
        return SimpleNamespace(
            now=lambda: SimpleNamespace(
                to_msg=lambda: Time(sec=12, nanosec=345_000_000)
            )
        )

    def get_logger(self):
        return self.logger


def make_snapshot():
    return SimpleNamespace(
        segment_name="PREGRASP AXIS",
        joint_names=tuple(f"joint_{index}" for index in range(1, 7)),
        rrt_tcp_positions=np.asarray(
            [[0.0, 0.0, 0.8], [0.4, 0.1, 1.0]],
            dtype=float,
        ),
        sample_times=np.asarray([0.0, 0.5], dtype=float),
        joint_positions=np.asarray(
            [np.zeros(6), np.full(6, 0.1)],
            dtype=float,
        ),
        joint_velocities=np.asarray(
            [np.zeros(6), np.full(6, 0.2)],
            dtype=float,
        ),
        tcp_positions=np.asarray(
            [[0.0, 0.0, 0.8], [0.4, 0.1, 1.0]],
            dtype=float,
        ),
        tcp_orientations_xyzw=np.asarray(
            [[0.0, 0.0, 0.0, 1.0], [0.0, 0.0, 0.0, 1.0]],
            dtype=float,
        ),
        target_position=np.asarray([0.4, 0.1, 1.15], dtype=float),
        pregrasp_position=np.asarray([0.4, 0.1, 1.0], dtype=float),
        minimum_clearance=0.032,
        closest_robot_center=np.asarray([0.2, 0.0, 0.9], dtype=float),
        closest_obstacle_center=np.asarray([0.2, 0.03, 0.9], dtype=float),
    )


def make_scene():
    pose = Pose()
    pose.position.x = 0.2
    pose.position.z = 1.0
    pose.orientation.w = 1.0
    obstacle = SimpleNamespace(
        shape=1,
        obstacle_class=2,
        pose=pose,
        dimensions=SimpleNamespace(x=0.02, y=0.0, z=0.0),
        safety_margin=0.02,
    )
    return SimpleNamespace(obstacles=[obstacle])


class MotionPlanningVisualizationTest(unittest.TestCase):
    def setUp(self):
        self.node = FakeNode()
        self.visualization = MotionPlanningVisualizationPublisher(self.node)

    def publisher(self, message_type, topic):
        return self.node.publishers[(message_type, topic)]

    def test_validated_plan_publishes_world_tcp_path_and_six_arm_joints(self):
        self.visualization.publish_plan(make_snapshot(), make_scene(), 4, 7)

        path = self.publisher(Path, "/harvest/planned_path").messages[-1]
        self.assertEqual(path.header.frame_id, "world")
        self.assertEqual(len(path.poses), 2)
        self.assertAlmostEqual(path.poses[-1].pose.position.x, 0.4)

        trajectory = self.publisher(
            JointTrajectory,
            "/harvest/planned_joint_trajectory",
        ).messages[-1]
        self.assertEqual(
            trajectory.joint_names,
            [f"joint_{index}" for index in range(1, 7)],
        )
        self.assertEqual(len(trajectory.points), 2)
        self.assertEqual(len(trajectory.points[-1].positions), 6)
        self.assertEqual(trajectory.points[-1].time_from_start.sec, 0)
        self.assertEqual(
            trajectory.points[-1].time_from_start.nanosec,
            500_000_000,
        )

    def test_markers_replace_previous_plan_and_include_safety_geometry(self):
        self.visualization.publish_plan(make_snapshot(), make_scene(), 4, 7)

        marker_array = self.publisher(
            MarkerArray,
            "/harvest/planning_markers",
        ).messages[-1]
        self.assertEqual(marker_array.markers[0].action, Marker.DELETEALL)
        namespaces = {marker.ns for marker in marker_array.markers}
        self.assertIn("target", namespaces)
        self.assertIn("pregrasp", namespaces)
        self.assertIn("rrt_solution", namespaces)
        self.assertIn("validated_tcp_path", namespaces)
        self.assertIn("minimum_clearance", namespaces)
        self.assertIn("obstacle_raw", namespaces)
        self.assertIn("obstacle_safety", namespaces)
        label = next(
            marker for marker in marker_array.markers if marker.ns == "plan_status"
        )
        self.assertIn("reset=4", label.text)
        self.assertIn("scene=7", label.text)
        self.assertIn("clearance=0.032 m", label.text)

    def test_clear_deletes_markers_and_empties_snapshot_topics(self):
        self.visualization.clear("unit test reset")

        marker_array = self.publisher(
            MarkerArray,
            "/harvest/planning_markers",
        ).messages[-1]
        self.assertEqual(len(marker_array.markers), 1)
        self.assertEqual(marker_array.markers[0].action, Marker.DELETEALL)
        path = self.publisher(Path, "/harvest/planned_path").messages[-1]
        trajectory = self.publisher(
            JointTrajectory,
            "/harvest/planned_joint_trajectory",
        ).messages[-1]
        self.assertEqual(path.header.frame_id, "world")
        self.assertEqual(path.poses, [])
        self.assertEqual(trajectory.joint_names, [])
        self.assertEqual(trajectory.points, [])

    def test_failure_marker_does_not_replace_last_valid_path(self):
        self.visualization.publish_plan(make_snapshot(), make_scene(), 4, 7)
        path_publisher = self.publisher(Path, "/harvest/planned_path")
        path_count = len(path_publisher.messages)

        self.visualization.publish_failure(
            np.asarray([0.1, 0.2, 0.3]),
            "301:APPROACH_UNREACHABLE",
            "RRT failed",
        )

        self.assertEqual(len(path_publisher.messages), path_count)
        marker_array = self.publisher(
            MarkerArray,
            "/harvest/planning_markers",
        ).messages[-1]
        namespaces = {marker.ns for marker in marker_array.markers}
        self.assertIn("planning_failure", namespaces)
        self.assertIn("validated_tcp_path", namespaces)


if __name__ == "__main__":
    unittest.main()
