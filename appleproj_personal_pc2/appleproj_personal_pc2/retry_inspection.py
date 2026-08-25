"""One-shot client for manually requesting a quality inspection retry."""

import argparse
import sys

import rclpy
from appleproj_interfaces.srv import RetryInspection
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.utilities import remove_ros_args


class RetryInspectionClient(Node):
    def __init__(self) -> None:
        super().__init__(
            "retry_inspection_client",
            parameter_overrides=[Parameter("use_sim_time", value=True)],
        )
        self.client = self.create_client(
            RetryInspection, "/quality/retry_inspection"
        )


def _parse_arguments(args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Request a quality inspection retry from GPU PC 1."
    )
    parser.add_argument("inspection_id")
    parser.add_argument("apple_id")
    parser.add_argument("reason")
    parser.add_argument(
        "--wait-timeout",
        type=float,
        default=5.0,
        help="Wall-time seconds to wait for the service and response (default: 5.0)",
    )
    parsed = parser.parse_args(remove_ros_args(args=args)[1:])
    for field_name in ("inspection_id", "apple_id", "reason"):
        if not getattr(parsed, field_name).strip():
            parser.error(f"{field_name} must not be empty")
    if parsed.wait_timeout <= 0.0:
        parser.error("--wait-timeout must be positive")
    return parsed


def main(args: list[str] | None = None) -> None:
    cli_args = sys.argv if args is None else args
    parsed = _parse_arguments(cli_args)
    rclpy.init(args=cli_args)
    node = RetryInspectionClient()
    exit_code = 1
    try:
        if not node.client.wait_for_service(timeout_sec=parsed.wait_timeout):
            node.get_logger().error("/quality/retry_inspection is unavailable")
            return

        request = RetryInspection.Request()
        request.inspection_id = parsed.inspection_id
        request.apple_id = parsed.apple_id
        request.reason = parsed.reason
        future = node.client.call_async(request)
        rclpy.spin_until_future_complete(
            node, future, timeout_sec=parsed.wait_timeout
        )
        if not future.done():
            node.get_logger().error("RetryInspection response timed out")
            return
        if future.exception() is not None:
            node.get_logger().error(
                f"RetryInspection call failed: {future.exception()}"
            )
            return
        response = future.result()
        if response is None:
            node.get_logger().error("RetryInspection call failed")
            return
        if response.accepted:
            node.get_logger().info(
                "retry accepted: "
                f"new_inspection_id={response.new_inspection_id} "
                f"message={response.message}"
            )
            exit_code = 0
        else:
            node.get_logger().warning(
                f"retry rejected: message={response.message}"
            )
    finally:
        node.destroy_node()
        rclpy.shutdown()
        if args is None:
            raise SystemExit(exit_code)
