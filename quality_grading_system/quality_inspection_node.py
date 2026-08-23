"""ROS 2 entry point for the GPU PC 2 quality-inspection pipeline.

The node validates and buffers ``InspectionImage`` messages, runs a configured
measurement model, aggregates representative frames, and publishes one
``QualityResult``.  Missing model heads remain explicitly unclassified.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Generic, TypeVar

from inspection_session import (
    InspectionContractError,
    InspectionFrame,
    InspectionStore,
)
from predictor import (
    FramePredictor,
    IndexedPrediction,
    PredictorNotConfigured,
    UnconfiguredPredictor,
    load_measurement_predictor,
    predict_declared_frames,
)
from quality_rules import FrameMeasurements, aggregate_measurement_frames


INPUT_TOPIC = "/quality/inspection_images"
OUTPUT_TOPIC = "/quality/results"
RESULT_QOS_DEPTH = 10
INPUT_QOS_DEPTH = 6
DEFAULT_CONFIDENCE_THRESHOLD = 0.5

try:
    import rclpy
    from appleproj_interfaces.msg import InspectionImage, QualityResult as QualityResultMessage
    from rclpy.node import Node
    from rclpy.parameter import Parameter
    from rclpy.qos import (
        DurabilityPolicy,
        HistoryPolicy,
        QoSProfile,
        ReliabilityPolicy,
    )

    _ROS_IMPORT_ERROR: ImportError | None = None
except ImportError as exc:  # Keep the transport-neutral core unit-testable.
    rclpy = None  # type: ignore[assignment]
    InspectionImage = None  # type: ignore[assignment,misc]
    QualityResultMessage = None  # type: ignore[assignment,misc]
    Parameter = None  # type: ignore[assignment,misc]
    QoSProfile = None  # type: ignore[assignment,misc]
    ReliabilityPolicy = None  # type: ignore[assignment,misc]
    DurabilityPolicy = None  # type: ignore[assignment,misc]
    HistoryPolicy = None  # type: ignore[assignment,misc]
    Node = object  # type: ignore[assignment,misc]
    _ROS_IMPORT_ERROR = exc


PredictionT = TypeVar("PredictionT")


class ProcessingState(str, Enum):
    """Observable state after one input frame is handled."""

    BUFFERING = "BUFFERING"
    DUPLICATE = "DUPLICATE"
    PREDICTED = "PREDICTED"
    PREDICTOR_UNAVAILABLE = "PREDICTOR_UNAVAILABLE"


@dataclass(frozen=True)
class ProcessingEvent(Generic[PredictionT]):
    state: ProcessingState
    inspection_id: str
    apple_id: str
    received_count: int
    total_frames: int
    predictions: tuple[IndexedPrediction[PredictionT], ...] = ()


def inspection_frame_from_message(message: Any) -> InspectionFrame:
    """Convert a ROS-like ``InspectionImage`` object into the core contract.

    The outer and compressed-image headers must carry the same timestamp and
    frame ID as decided for the MVP contract.
    """

    outer_header = getattr(message, "header", None)
    inner_header = getattr(message.image, "header", None)
    if outer_header is not None and inner_header is not None:
        outer_signature = _header_signature(outer_header)
        inner_signature = _header_signature(inner_header)
        if outer_signature != inner_signature:
            raise InspectionContractError(
                "InspectionImage.header and CompressedImage.header must have identical stamp and frame_id"
            )

    return InspectionFrame(
        inspection_id=message.inspection_id,
        apple_id=message.apple_id,
        frame_index=int(message.frame_index),
        total_frames=int(message.total_frames),
        image_data=bytes(message.image.data),
        image_format=message.image.format,
    )


def _header_signature(header: Any) -> tuple[int, int, str]:
    stamp = header.stamp
    return int(stamp.sec), int(stamp.nanosec), str(header.frame_id)


class InspectionCoordinator(Generic[PredictionT]):
    """Connect validated frame storage to a replaceable measurement model."""

    def __init__(self, predictor: FramePredictor[PredictionT]) -> None:
        self._store = InspectionStore()
        self._predictor = predictor
        self._attempted_inspections: set[str] = set()

    @property
    def store(self) -> InspectionStore:
        return self._store

    def handle(self, frame: InspectionFrame) -> ProcessingEvent[PredictionT]:
        acceptance = self._store.accept(frame)
        session = acceptance.session

        if not acceptance.is_new_frame:
            return ProcessingEvent(
                ProcessingState.DUPLICATE,
                session.inspection_id,
                session.apple_id,
                session.received_count,
                session.total_frames,
            )
        if not session.has_all_declared_frames:
            return ProcessingEvent(
                ProcessingState.BUFFERING,
                session.inspection_id,
                session.apple_id,
                session.received_count,
                session.total_frames,
            )
        if session.inspection_id in self._attempted_inspections:
            return ProcessingEvent(
                ProcessingState.DUPLICATE,
                session.inspection_id,
                session.apple_id,
                session.received_count,
                session.total_frames,
            )

        self._attempted_inspections.add(session.inspection_id)
        try:
            predictions = predict_declared_frames(session, self._predictor)
        except PredictorNotConfigured:
            return ProcessingEvent(
                ProcessingState.PREDICTOR_UNAVAILABLE,
                session.inspection_id,
                session.apple_id,
                session.received_count,
                session.total_frames,
            )
        return ProcessingEvent(
            ProcessingState.PREDICTED,
            session.inspection_id,
            session.apple_id,
            session.received_count,
            session.total_frames,
            predictions,
        )


def make_result_qos() -> Any:
    """Build the approved temporary reliable result QoS profile."""

    if QoSProfile is None:
        raise RuntimeError("rclpy is required to construct the result QoS profile")
    return QoSProfile(
        reliability=ReliabilityPolicy.RELIABLE,
        durability=DurabilityPolicy.VOLATILE,
        history=HistoryPolicy.KEEP_LAST,
        depth=RESULT_QOS_DEPTH,
    )


def make_input_qos() -> Any:
    """Build the decided reliable six-frame inspection-image QoS profile."""

    if QoSProfile is None:
        raise RuntimeError("rclpy is required to construct the input QoS profile")
    return QoSProfile(
        reliability=ReliabilityPolicy.RELIABLE,
        durability=DurabilityPolicy.VOLATILE,
        history=HistoryPolicy.KEEP_LAST,
        depth=INPUT_QOS_DEPTH,
    )


class QualityInspectionNode(Node):  # type: ignore[misc]
    """GPU PC 2 ROS node for frame ingestion and inference dispatch."""

    def __init__(self, predictor: FramePredictor[Any] | None = None) -> None:
        if _ROS_IMPORT_ERROR is not None:
            raise RuntimeError(
                "ROS 2 Python packages are unavailable; source ROS 2 Jazzy and "
                "the built appleproj_interfaces workspace first"
            ) from _ROS_IMPORT_ERROR

        super().__init__(
            "quality_inspection_node",
            parameter_overrides=[Parameter("use_sim_time", value=True)],
            automatically_declare_parameters_from_overrides=True,
        )
        for name, default in (
            ("model_path", ""),
            ("model_backend", "auto"),
            ("confidence_threshold", DEFAULT_CONFIDENCE_THRESHOLD),
        ):
            if not self.has_parameter(name):
                self.declare_parameter(name, default)
        configured_predictor = predictor
        if configured_predictor is None:
            model_path = str(self.get_parameter("model_path").value)
            backend = str(self.get_parameter("model_backend").value)
            configured_predictor = (
                load_measurement_predictor(model_path, backend=backend)
                if model_path
                else UnconfiguredPredictor()
            )
        self._confidence_threshold = float(self.get_parameter("confidence_threshold").value)
        self._coordinator = InspectionCoordinator(configured_predictor)
        self._result_publisher = self.create_publisher(
            QualityResultMessage,
            OUTPUT_TOPIC,
            make_result_qos(),
        )
        self._inspection_subscription = self.create_subscription(
            InspectionImage,
            INPUT_TOPIC,
            self._on_inspection_image,
            make_input_qos(),
        )
        self.get_logger().info(
            f"GPU PC 2 quality node ready: {INPUT_TOPIC} -> {OUTPUT_TOPIC}; use_sim_time=true"
        )

    def _on_inspection_image(self, message: Any) -> None:
        try:
            frame = inspection_frame_from_message(message)
            event = self._coordinator.handle(frame)
        except InspectionContractError as exc:
            self.get_logger().error(f"Rejected InspectionImage contract: {exc}")
            return
        except Exception as exc:  # A configured model failure is not a contract failure.
            self.get_logger().error(f"Inspection inference failed: {exc}")
            return

        if event.state is ProcessingState.BUFFERING:
            self.get_logger().debug(
                f"Buffering {event.inspection_id}: "
                f"{event.received_count}/{event.total_frames} frames"
            )
        elif event.state is ProcessingState.DUPLICATE:
            self.get_logger().warning(
                f"Ignored duplicate frame for inspection {event.inspection_id}"
            )
        elif event.state is ProcessingState.PREDICTOR_UNAVAILABLE:
            self.get_logger().warning(
                f"Inspection {event.inspection_id} is buffered, but no approved model is configured; "
                "QualityResult was not published"
            )
        elif event.state is ProcessingState.PREDICTED:
            if not all(isinstance(item.value, FrameMeasurements) for item in event.predictions):
                self.get_logger().error(
                    f"Inspection {event.inspection_id} predictor returned an unsupported output type"
                )
                return
            result = aggregate_measurement_frames(
                (item.value for item in event.predictions),
                (item.frame_index for item in event.predictions),
                confidence_threshold=self._confidence_threshold,
            )
            self._publish_result(event, result)
            self._coordinator.store.pop(event.inspection_id)

    def _publish_result(self, event: ProcessingEvent[Any], result: Any) -> None:
        message = QualityResultMessage()
        now = self.get_clock().now().to_msg()
        message.header.stamp = now
        message.header.frame_id = "quality_grading"
        message.inspection_id = event.inspection_id
        message.apple_id = event.apple_id
        message.grade = (
            int(getattr(QualityResultMessage, result.grade.value))
            if result.grade is not None
            else 0
        )
        message.confidence = float(result.confidence) if result.confidence is not None else float("nan")
        measurements = result.measurements
        message.color_ratio = float(measurements.color_ratio) if measurements else float("nan")
        message.diameter_mm = float(measurements.diameter_mm) if measurements else float("nan")
        message.damage_area_cm2 = float(measurements.damage_area_cm2) if measurements else float("nan")
        message.frames_used = len(result.frames_used)
        message.frame_indices = list(result.frames_used)
        message.result_timestamp = now
        message.status = int(getattr(QualityResultMessage, result.status.value))
        self._result_publisher.publish(message)
        self.get_logger().info(
            f"Published {result.status.value} for {event.inspection_id}: "
            f"grade={result.grade.value if result.grade else 'NONE'}, frames={list(result.frames_used)}"
        )


def main(args: list[str] | None = None) -> None:
    """Run the ROS 2 node with the safe, unconfigured predictor."""

    if rclpy is None:
        raise RuntimeError(
            "ROS 2 Python packages are unavailable; source ROS 2 Jazzy and the workspace"
        ) from _ROS_IMPORT_ERROR

    rclpy.init(args=args)
    node = QualityInspectionNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
