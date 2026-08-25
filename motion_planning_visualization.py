"""RViz messages for GPU PC 1 motion-planning diagnostics.

This module only translates already validated planner output into ROS messages.
It never participates in goal admission, collision checking, or robot control.
"""

import math

from geometry_msgs.msg import Point, PoseStamped
from nav_msgs.msg import Path
from rclpy.qos import (
    DurabilityPolicy,
    HistoryPolicy,
    QoSProfile,
    ReliabilityPolicy,
)
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from visualization_msgs.msg import Marker, MarkerArray


WORLD_FRAME = "world"
MARKERS_TOPIC = "/harvest/planning_markers"
PATH_TOPIC = "/harvest/planned_path"
JOINT_TRAJECTORY_TOPIC = "/harvest/planned_joint_trajectory"


def visualization_qos():
    """Latest validated plan snapshot, retained for late RViz subscribers."""
    return QoSProfile(
        history=HistoryPolicy.KEEP_LAST,
        depth=1,
        reliability=ReliabilityPolicy.RELIABLE,
        durability=DurabilityPolicy.TRANSIENT_LOCAL,
    )


def _duration_from_seconds(seconds):
    seconds = max(0.0, float(seconds))
    sec = int(math.floor(seconds))
    nanosec = int(round((seconds - sec) * 1_000_000_000.0))
    if nanosec >= 1_000_000_000:
        sec += 1
        nanosec -= 1_000_000_000
    return sec, nanosec


def _copy_pose(target, source):
    target.position.x = float(source.position.x)
    target.position.y = float(source.position.y)
    target.position.z = float(source.position.z)
    target.orientation.x = float(source.orientation.x)
    target.orientation.y = float(source.orientation.y)
    target.orientation.z = float(source.orientation.z)
    target.orientation.w = float(source.orientation.w)


def _point(values):
    value = Point()
    value.x = float(values[0])
    value.y = float(values[1])
    value.z = float(values[2])
    return value


def _set_color(marker, red, green, blue, alpha):
    marker.color.r = float(red)
    marker.color.g = float(green)
    marker.color.b = float(blue)
    marker.color.a = float(alpha)


def _quaternion_multiply_xyzw(first, second):
    x1, y1, z1, w1 = first
    x2, y2, z2, w2 = second
    return (
        w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
        w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
        w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
        w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
    )


class MotionPlanningVisualizationPublisher:
    """Non-authoritative publisher isolated from motion execution."""

    def __init__(self, node):
        self._node = node
        qos = visualization_qos()
        self._markers = node.create_publisher(MarkerArray, MARKERS_TOPIC, qos)
        self._path = node.create_publisher(Path, PATH_TOPIC, qos)
        self._joint_trajectory = node.create_publisher(
            JointTrajectory,
            JOINT_TRAJECTORY_TOPIC,
            qos,
        )
        self._last_plan_markers = []

    def _header(self, stamp):
        header = PoseStamped().header
        header.stamp = stamp
        header.frame_id = WORLD_FRAME
        return header

    def _base_marker(self, stamp, namespace, marker_id, marker_type):
        marker = Marker()
        marker.header = self._header(stamp)
        marker.ns = str(namespace)
        marker.id = int(marker_id)
        marker.type = int(marker_type)
        marker.action = Marker.ADD
        marker.pose.orientation.w = 1.0
        marker.lifetime.sec = 0
        marker.lifetime.nanosec = 0
        return marker

    def clear(self, reason=""):
        """Remove stale plans after reset or planning-scene invalidation."""
        try:
            stamp = self._node.get_clock().now().to_msg()
            marker = self._base_marker(stamp, "planning", 0, Marker.SPHERE)
            marker.action = Marker.DELETEALL
            self._markers.publish(MarkerArray(markers=[marker]))
            self._last_plan_markers = []

            path = Path()
            path.header = self._header(stamp)
            self._path.publish(path)

            trajectory = JointTrajectory()
            trajectory.header = self._header(stamp)
            self._joint_trajectory.publish(trajectory)
            if reason:
                self._node.get_logger().info(
                    f"motion planning visualization cleared: {reason}"
                )
        except Exception as error:
            self._node.get_logger().warning(
                f"motion planning visualization clear failed: {error}"
            )

    def publish_failure(self, target_position, error_code, message):
        """Keep the last valid path and add a diagnostic marker at the goal."""
        try:
            stamp = self._node.get_clock().now().to_msg()
            point = self._base_marker(stamp, "planning_failure", 0, Marker.SPHERE)
            point.pose.position.x = float(target_position[0])
            point.pose.position.y = float(target_position[1])
            point.pose.position.z = float(target_position[2])
            point.scale.x = point.scale.y = point.scale.z = 0.06
            _set_color(point, 1.0, 0.0, 0.8, 0.95)

            text = self._base_marker(
                stamp,
                "planning_failure",
                1,
                Marker.TEXT_VIEW_FACING,
            )
            text.pose.position.x = float(target_position[0])
            text.pose.position.y = float(target_position[1])
            text.pose.position.z = float(target_position[2]) + 0.10
            text.scale.z = 0.035
            text.text = f"{error_code}: {message}"
            _set_color(text, 1.0, 0.2, 0.8, 1.0)
            markers = [*self._last_plan_markers, point, text]
            self._markers.publish(MarkerArray(markers=markers))
        except Exception as error:
            self._node.get_logger().warning(
                f"motion planning failure marker publish failed: {error}"
            )

    def publish_plan(self, snapshot, scene, reset_id, scene_version):
        """Publish one collision-validated plan snapshot."""
        try:
            stamp = self._node.get_clock().now().to_msg()
            path = self._path_message(snapshot, stamp)
            trajectory = self._joint_trajectory_message(snapshot, stamp)
            markers = self._marker_array(
                snapshot,
                scene,
                stamp,
                reset_id,
                scene_version,
            )
            self._last_plan_markers = list(markers.markers)
            self._markers.publish(markers)
            self._path.publish(path)
            self._joint_trajectory.publish(trajectory)
        except Exception as error:
            self._node.get_logger().warning(
                f"motion planning visualization publish failed: {error}"
            )

    def _path_message(self, snapshot, stamp):
        path = Path()
        path.header = self._header(stamp)
        for position, orientation in zip(
            snapshot.tcp_positions,
            snapshot.tcp_orientations_xyzw,
        ):
            pose = PoseStamped()
            pose.header = path.header
            pose.pose.position.x = float(position[0])
            pose.pose.position.y = float(position[1])
            pose.pose.position.z = float(position[2])
            pose.pose.orientation.x = float(orientation[0])
            pose.pose.orientation.y = float(orientation[1])
            pose.pose.orientation.z = float(orientation[2])
            pose.pose.orientation.w = float(orientation[3])
            path.poses.append(pose)
        return path

    def _joint_trajectory_message(self, snapshot, stamp):
        trajectory = JointTrajectory()
        trajectory.header = self._header(stamp)
        trajectory.joint_names = list(snapshot.joint_names)
        for relative_time, positions, velocities in zip(
            snapshot.sample_times,
            snapshot.joint_positions,
            snapshot.joint_velocities,
        ):
            point = JointTrajectoryPoint()
            point.positions = [float(value) for value in positions]
            point.velocities = [float(value) for value in velocities]
            point.time_from_start.sec, point.time_from_start.nanosec = (
                _duration_from_seconds(relative_time)
            )
            trajectory.points.append(point)
        return trajectory

    def _marker_array(self, snapshot, scene, stamp, reset_id, scene_version):
        clear = self._base_marker(stamp, "planning", 0, Marker.SPHERE)
        clear.action = Marker.DELETEALL
        markers = [clear]
        markers.extend(self._obstacle_markers(scene, stamp))

        target = self._base_marker(stamp, "target", 0, Marker.SPHERE)
        target.pose.position.x = float(snapshot.target_position[0])
        target.pose.position.y = float(snapshot.target_position[1])
        target.pose.position.z = float(snapshot.target_position[2])
        target.scale.x = target.scale.y = target.scale.z = 0.08
        _set_color(target, 0.95, 0.05, 0.05, 0.95)
        markers.append(target)

        pregrasp = self._base_marker(stamp, "pregrasp", 0, Marker.SPHERE)
        pregrasp.pose.position.x = float(snapshot.pregrasp_position[0])
        pregrasp.pose.position.y = float(snapshot.pregrasp_position[1])
        pregrasp.pose.position.z = float(snapshot.pregrasp_position[2])
        pregrasp.scale.x = pregrasp.scale.y = pregrasp.scale.z = 0.04
        _set_color(pregrasp, 0.0, 0.9, 0.95, 0.95)
        markers.append(pregrasp)

        approach = self._base_marker(stamp, "approach", 0, Marker.ARROW)
        approach.points = [
            _point(snapshot.pregrasp_position),
            _point(snapshot.target_position),
        ]
        approach.scale.x = 0.012
        approach.scale.y = 0.025
        approach.scale.z = 0.035
        _set_color(approach, 0.0, 0.85, 0.95, 0.9)
        markers.append(approach)

        rrt_path = self._base_marker(stamp, "rrt_solution", 0, Marker.LINE_STRIP)
        rrt_path.scale.x = 0.008
        rrt_path.points = [_point(value) for value in snapshot.rrt_tcp_positions]
        _set_color(rrt_path, 0.1, 0.45, 1.0, 0.8)
        markers.append(rrt_path)

        tcp_path = self._base_marker(stamp, "validated_tcp_path", 0, Marker.LINE_STRIP)
        tcp_path.scale.x = 0.014
        tcp_path.points = [_point(value) for value in snapshot.tcp_positions]
        _set_color(tcp_path, 0.1, 1.0, 0.2, 0.95)
        markers.append(tcp_path)

        if (
            snapshot.closest_robot_center is not None
            and snapshot.closest_obstacle_center is not None
        ):
            clearance = self._base_marker(
                stamp,
                "minimum_clearance",
                0,
                Marker.LINE_LIST,
            )
            clearance.scale.x = 0.010
            clearance.points = [
                _point(snapshot.closest_robot_center),
                _point(snapshot.closest_obstacle_center),
            ]
            _set_color(clearance, 1.0, 0.2, 0.8, 0.95)
            markers.append(clearance)

        label = self._base_marker(
            stamp,
            "plan_status",
            0,
            Marker.TEXT_VIEW_FACING,
        )
        label.pose.position.x = float(snapshot.pregrasp_position[0])
        label.pose.position.y = float(snapshot.pregrasp_position[1])
        label.pose.position.z = float(snapshot.pregrasp_position[2]) + 0.10
        label.scale.z = 0.035
        label.text = (
            f"{snapshot.segment_name}  reset={int(reset_id)} "
            f"scene={int(scene_version)}  "
            f"clearance={float(snapshot.minimum_clearance):.3f} m"
        )
        _set_color(label, 1.0, 1.0, 1.0, 1.0)
        markers.append(label)
        return MarkerArray(markers=markers)

    def _obstacle_markers(self, scene, stamp):
        markers = []
        if scene is None:
            return markers
        for index, obstacle in enumerate(scene.obstacles):
            raw = self._obstacle_marker(
                obstacle,
                stamp,
                "obstacle_raw",
                index,
                0.0,
            )
            safety = self._obstacle_marker(
                obstacle,
                stamp,
                "obstacle_safety",
                index,
                float(obstacle.safety_margin),
            )
            if int(obstacle.obstacle_class) == 1:
                _set_color(raw, 0.55, 0.27, 0.08, 0.55)
            else:
                _set_color(raw, 0.95, 0.65, 0.12, 0.55)
            _set_color(safety, 1.0, 0.15, 0.05, 0.14)
            markers.extend([raw, safety])
        return markers

    def _obstacle_marker(self, obstacle, stamp, namespace, marker_id, margin):
        shape = int(obstacle.shape)
        if shape == 1:
            marker_type = Marker.SPHERE
        elif shape == 2:
            marker_type = Marker.CUBE
        else:
            marker_type = Marker.CYLINDER
        marker = self._base_marker(stamp, namespace, marker_id, marker_type)
        _copy_pose(marker.pose, obstacle.pose)

        if shape == 1:
            diameter = 2.0 * (float(obstacle.dimensions.x) + margin)
            marker.scale.x = marker.scale.y = marker.scale.z = diameter
        elif shape == 2:
            marker.scale.x = float(obstacle.dimensions.x) + 2.0 * margin
            marker.scale.y = float(obstacle.dimensions.y) + 2.0 * margin
            marker.scale.z = float(obstacle.dimensions.z) + 2.0 * margin
        else:
            radius = float(obstacle.dimensions.x) + margin
            marker.scale.x = marker.scale.y = 2.0 * radius
            marker.scale.z = float(obstacle.dimensions.y) + 2.0 * radius
            source = (
                marker.pose.orientation.x,
                marker.pose.orientation.y,
                marker.pose.orientation.z,
                marker.pose.orientation.w,
            )
            rotated = _quaternion_multiply_xyzw(
                source,
                (-math.sqrt(0.5), 0.0, 0.0, math.sqrt(0.5)),
            )
            marker.pose.orientation.x = rotated[0]
            marker.pose.orientation.y = rotated[1]
            marker.pose.orientation.z = rotated[2]
            marker.pose.orientation.w = rotated[3]
        return marker
