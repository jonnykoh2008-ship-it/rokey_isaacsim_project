"""Personal PC 2 ROS node for monitoring quality results and checkpoints."""

from functools import partial

import rclpy
from appleproj_interfaces.msg import CheckpointEvent, QualityResult
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.qos import qos_profile_system_default

from .monitor_state import MonitorNotice, MonitorState


GRADE_NAMES = {
    QualityResult.HIGH: "HIGH",
    QualityResult.MEDIUM: "MEDIUM",
    QualityResult.LOW: "LOW",
}

STATUS_NAMES = {
    QualityResult.VALID: "VALID",
    QualityResult.RECHECK: "RECHECK",
    QualityResult.UNCLASSIFIED: "UNCLASSIFIED",
    QualityResult.TIMEOUT: "TIMEOUT",
    QualityResult.LATE_RESULT: "LATE_RESULT",
    QualityResult.ID_MISMATCH: "ID_MISMATCH",
    QualityResult.INSUFFICIENT_VIEWS: "INSUFFICIENT_VIEWS",
}

EVENT_NAMES = {
    CheckpointEvent.ENTER: "ENTER",
    CheckpointEvent.EXIT: "EXIT",
}


def _stamp_to_nanoseconds(stamp: object) -> int:
    return int(stamp.sec) * 1_000_000_000 + int(stamp.nanosec)


class QualityMonitor(Node):
    """Display results and correlate them with conveyor checkpoint events."""

    def __init__(self) -> None:
        super().__init__(
            "quality_monitor",
            parameter_overrides=[Parameter("use_sim_time", value=True)],
        )
        self.declare_parameter("deadline_checkpoint_id", "")
        self.declare_parameter("result_deadline_sec", 0.5)

        checkpoint_id = str(self.get_parameter("deadline_checkpoint_id").value)
        deadline_sec = float(self.get_parameter("result_deadline_sec").value)
        if deadline_sec <= 0.0:
            raise ValueError("result_deadline_sec must be positive")

        self._state = MonitorState(
            deadline_ns=int(deadline_sec * 1_000_000_000),
            deadline_checkpoint_id=checkpoint_id,
        )
        self.create_subscription(
            QualityResult,
            "/quality/results",
            self._on_result,
            qos_profile_system_default,
        )
        self.create_subscription(
            CheckpointEvent,
            "/conveyor/checkpoint_events",
            self._on_checkpoint,
            qos_profile_system_default,
        )
        self.create_timer(min(deadline_sec / 5.0, 0.1), self._check_deadlines)

        self.get_logger().info(
            "Personal PC 2 monitor started with use_sim_time=true"
        )
        if not self._state.deadline_enabled:
            self.get_logger().warning(
                "deadline_checkpoint_id is TBD and unset; local TIMEOUT/LATE_RESULT "
                "detection is disabled"
            )

    def _on_result(self, message: QualityResult) -> None:
        now_ns = self.get_clock().now().nanoseconds
        grade = GRADE_NAMES.get(message.grade, f"UNKNOWN({message.grade})")
        status = STATUS_NAMES.get(message.status, f"UNKNOWN({message.status})")
        self.get_logger().info(
            "quality result: "
            f"inspection={message.inspection_id} apple={message.apple_id} "
            f"grade={grade} status={status} confidence={message.confidence:.3f} "
            f"color_ratio={message.color_ratio:.3f} "
            f"diameter_mm={message.diameter_mm:.2f} "
            f"damage_area_cm2={message.damage_area_cm2:.3f} "
            f"frames={message.frames_used} indices={list(message.frame_indices)}"
        )
        self._report(
            self._state.process_result(
                inspection_id=message.inspection_id,
                apple_id=message.apple_id,
                received_at_ns=now_ns,
            )
        )

    def _on_checkpoint(self, message: CheckpointEvent) -> None:
        event = EVENT_NAMES.get(message.event, f"UNKNOWN({message.event})")
        self.get_logger().info(
            "checkpoint event: "
            f"apple={message.apple_id} checkpoint={message.checkpoint_id} "
            f"event={event}"
        )
        self._report(
            self._state.process_checkpoint(
                apple_id=message.apple_id,
                checkpoint_id=message.checkpoint_id,
                event=message.event,
                timestamp_ns=_stamp_to_nanoseconds(message.header.stamp),
            )
        )

    def _check_deadlines(self) -> None:
        if self._state.deadline_enabled:
            self._report(self._state.expire(self.get_clock().now().nanoseconds))

    def _report(self, notices: list[MonitorNotice]) -> None:
        logger = self.get_logger()
        log_methods = {
            "info": logger.info,
            "warning": logger.warning,
            "error": logger.error,
        }
        for notice in notices:
            log_methods[notice.level](f"{notice.code}: {notice.message}")


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)
    node = QualityMonitor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
