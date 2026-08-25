"""Development-only publisher for Personal PC 2 integration checks."""

import argparse
import sys

import rclpy
from appleproj_interfaces.msg import CheckpointEvent, QualityResult
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.qos import qos_profile_system_default
from rclpy.utilities import remove_ros_args


GRADE_VALUES = {
    "HIGH": QualityResult.HIGH,
    "MEDIUM": QualityResult.MEDIUM,
    "LOW": QualityResult.LOW,
}

STATUS_VALUES = {
    "VALID": QualityResult.VALID,
    "RECHECK": QualityResult.RECHECK,
    "UNCLASSIFIED": QualityResult.UNCLASSIFIED,
    "TIMEOUT": QualityResult.TIMEOUT,
    "LATE_RESULT": QualityResult.LATE_RESULT,
    "ID_MISMATCH": QualityResult.ID_MISMATCH,
    "INSUFFICIENT_VIEWS": QualityResult.INSUFFICIENT_VIEWS,
}

CHECKPOINT_VALUES = {
    "NONE": None,
    "ENTER": CheckpointEvent.ENTER,
    "EXIT": CheckpointEvent.EXIT,
}


def _parse_arguments(args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Publish one development-only QualityResult and optional "
            "CheckpointEvent. Do not run beside production publishers."
        )
    )
    parser.add_argument("--inspection-id", required=True)
    parser.add_argument("--apple-id", required=True)
    parser.add_argument("--grade", choices=GRADE_VALUES, default="HIGH")
    parser.add_argument("--status", choices=STATUS_VALUES, default="VALID")
    parser.add_argument(
        "--checkpoint-event", choices=CHECKPOINT_VALUES, default="NONE"
    )
    parser.add_argument("--checkpoint-id", default="")
    parsed = parser.parse_args(remove_ros_args(args=args)[1:])
    if not parsed.inspection_id.strip():
        parser.error("--inspection-id must not be empty")
    if not parsed.apple_id.strip():
        parser.error("--apple-id must not be empty")
    if parsed.checkpoint_event != "NONE" and not parsed.checkpoint_id.strip():
        parser.error(
            "--checkpoint-id is required when --checkpoint-event is used"
        )
    return parsed


class MockQualitySource(Node):
    """Publish one deterministic message set after ROS discovery."""

    def __init__(self, parsed: argparse.Namespace) -> None:
        super().__init__(
            "mock_quality_source",
            parameter_overrides=[Parameter("use_sim_time", value=True)],
        )
        self._parsed = parsed
        self._result_publisher = self.create_publisher(
            QualityResult, "/quality/results", qos_profile_system_default
        )
        self._checkpoint_publisher = self.create_publisher(
            CheckpointEvent,
            "/conveyor/checkpoint_events",
            qos_profile_system_default,
        )
        self._published = False
        self._timer = self.create_timer(0.5, self._publish_once)

    @property
    def published(self) -> bool:
        return self._published

    def _publish_once(self) -> None:
        if self._published:
            return
        stamp = self.get_clock().now().to_msg()

        checkpoint_value = CHECKPOINT_VALUES[self._parsed.checkpoint_event]
        if checkpoint_value is not None:
            checkpoint = CheckpointEvent()
            checkpoint.header.stamp = stamp
            checkpoint.apple_id = self._parsed.apple_id
            checkpoint.checkpoint_id = self._parsed.checkpoint_id
            checkpoint.event = checkpoint_value
            self._checkpoint_publisher.publish(checkpoint)

        result = QualityResult()
        result.header.stamp = stamp
        result.inspection_id = self._parsed.inspection_id
        result.apple_id = self._parsed.apple_id
        result.grade = GRADE_VALUES[self._parsed.grade]
        result.confidence = 0.9
        result.color_ratio = 0.8
        result.diameter_mm = 75.0
        result.damage_area_cm2 = 1.0
        result.frames_used = 4
        result.frame_indices = [0, 1, 2, 3]
        result.result_timestamp = stamp
        result.status = STATUS_VALUES[self._parsed.status]
        self._result_publisher.publish(result)
        self._published = True
        self._timer.cancel()
        self.get_logger().info("development-only mock messages published")


def main(args: list[str] | None = None) -> None:
    cli_args = sys.argv if args is None else args
    parsed = _parse_arguments(cli_args)
    rclpy.init(args=cli_args)
    node = MockQualitySource(parsed)
    try:
        while rclpy.ok() and not node.published:
            rclpy.spin_once(node, timeout_sec=0.1)
    finally:
        node.destroy_node()
        rclpy.shutdown()
