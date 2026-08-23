"""ROS 2 entry point for the GPU PC 2 quality-inspection pipeline."""

from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Any, Generic, TypeVar

from depth_geometry import GeometryMeasurementError, combine_prediction_with_geometry
from inspection_session import (
    InspectionCompletion,
    InspectionContractError,
    InspectionFrame,
    InspectionSession,
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
from quality_rules import (
    QualityResult as CoreQualityResult,
    ResultStatus,
    aggregate_measurement_frames,
)


INPUT_TOPIC = "/quality/inspection_images"
COMPLETION_TOPIC = "/quality/inspection_completed"
OUTPUT_TOPIC = "/quality/results"
RESULT_QOS_DEPTH = 10
COMPLETION_QOS_DEPTH = 10
INPUT_QOS_DEPTH = 6
DEFAULT_CONFIDENCE_THRESHOLD = 0.5
DEFAULT_STALE_SESSION_TIMEOUT_SEC = 3.0
RECENT_FINALIZED_LIMIT = 64

try:
    import rclpy
    from appleproj_interfaces.msg import (
        InspectionCompleted,
        InspectionImage,
        QualityResult as QualityResultMessage,
    )
    from rclpy.clock import Clock, ClockType
    from rclpy.node import Node
    from rclpy.parameter import Parameter
    from rclpy.qos import (
        DurabilityPolicy,
        HistoryPolicy,
        QoSProfile,
        ReliabilityPolicy,
    )

    _ROS_IMPORT_ERROR: ImportError | None = None
except ImportError as exc:
    rclpy = None  # type: ignore[assignment]
    InspectionCompleted = None  # type: ignore[assignment,misc]
    InspectionImage = None  # type: ignore[assignment,misc]
    QualityResultMessage = None  # type: ignore[assignment,misc]
    Clock = None  # type: ignore[assignment,misc]
    ClockType = None  # type: ignore[assignment,misc]
    Parameter = None  # type: ignore[assignment,misc]
    QoSProfile = None  # type: ignore[assignment,misc]
    ReliabilityPolicy = None  # type: ignore[assignment,misc]
    DurabilityPolicy = None  # type: ignore[assignment,misc]
    HistoryPolicy = None  # type: ignore[assignment,misc]
    Node = object  # type: ignore[assignment,misc]
    _ROS_IMPORT_ERROR = exc


PredictionT = TypeVar("PredictionT")


class ProcessingState(str, Enum):
    BUFFERING = "BUFFERING"
    DUPLICATE = "DUPLICATE"
    PREDICTED = "PREDICTED"
    PREDICTOR_UNAVAILABLE = "PREDICTOR_UNAVAILABLE"
    TIMEOUT = "TIMEOUT"
    STALE = "STALE"
    FINALIZED = "FINALIZED"


@dataclass(frozen=True)
class ProcessingEvent(Generic[PredictionT]):
    state: ProcessingState
    inspection_id: str
    apple_id: str
    received_count: int
    total_frames: int
    predictions: tuple[IndexedPrediction[PredictionT], ...] = ()
    deadline_time_ns: int | None = None


def _header_signature(header: Any) -> tuple[int, int, str]:
    stamp = header.stamp
    return int(stamp.sec), int(stamp.nanosec), str(header.frame_id)


def _stamp_to_ns(stamp: Any) -> int:
    return int(stamp.sec) * 1_000_000_000 + int(stamp.nanosec)


def inspection_frame_from_message(message: Any) -> InspectionFrame:
    """Validate and convert the synchronized custom RGB-D message."""

    components = (
        ("InspectionImage", message.header),
        ("CompressedImage", message.image.header),
        ("apple_mask", message.apple_mask.header),
        ("aligned_depth", message.aligned_depth.header),
        ("CameraInfo", message.camera_info.header),
    )
    signatures = [(name, _header_signature(header)) for name, header in components]
    expected = signatures[0][1]
    mismatched = [name for name, signature in signatures[1:] if signature != expected]
    if mismatched:
        raise InspectionContractError(
            "all InspectionImage component headers must have identical stamp and frame_id; "
            f"mismatched={mismatched}"
        )

    return InspectionFrame(
        inspection_id=message.inspection_id,
        apple_id=message.apple_id,
        frame_index=int(message.frame_index),
        total_frames=int(message.total_frames),
        image_data=bytes(message.image.data),
        image_format=str(message.image.format),
        apple_mask_data=bytes(message.apple_mask.data),
        apple_mask_format=str(message.apple_mask.format),
        depth_data=bytes(message.aligned_depth.data),
        depth_format=str(message.aligned_depth.format),
        camera_width=int(message.camera_info.width),
        camera_height=int(message.camera_info.height),
        camera_k=tuple(float(value) for value in message.camera_info.k),
        camera_p=tuple(float(value) for value in message.camera_info.p),
        stamp_ns=_stamp_to_ns(message.header.stamp),
        frame_id=str(message.header.frame_id),
    )


def inspection_completion_from_message(message: Any) -> InspectionCompletion:
    return InspectionCompletion(
        inspection_id=str(message.inspection_id),
        apple_id=str(message.apple_id),
        total_frames=int(message.total_frames),
        roi_exit_time_ns=_stamp_to_ns(message.header.stamp),
        frame_id=str(message.header.frame_id),
    )


class InspectionCoordinator(Generic[PredictionT]):
    """Own inspection lifecycle without depending on ROS message classes."""

    def __init__(self, predictor: FramePredictor[PredictionT]) -> None:
        self._store = InspectionStore()
        self._predictor = predictor
        self._last_wall_activity_ns: dict[str, int] = {}
        self._recent_finalized: deque[str] = deque(maxlen=RECENT_FINALIZED_LIMIT)
        self._recent_finalized_set: set[str] = set()

    @property
    def store(self) -> InspectionStore:
        return self._store

    def _event(
        self,
        state: ProcessingState,
        session: InspectionSession,
        predictions: tuple[IndexedPrediction[PredictionT], ...] = (),
    ) -> ProcessingEvent[PredictionT]:
        deadline = session.completion.deadline_time_ns if session.completion else None
        return ProcessingEvent(
            state=state,
            inspection_id=session.inspection_id,
            apple_id=session.apple_id,
            received_count=session.received_count,
            total_frames=session.total_frames,
            predictions=predictions,
            deadline_time_ns=deadline,
        )

    def _is_recently_finalized(self, inspection_id: str) -> bool:
        return inspection_id in self._recent_finalized_set

    def _touch(self, inspection_id: str, wall_time_ns: int | None) -> None:
        self._last_wall_activity_ns[inspection_id] = (
            time.monotonic_ns() if wall_time_ns is None else wall_time_ns
        )

    def handle_frame(
        self,
        frame: InspectionFrame,
        simulation_time_ns: int,
        wall_time_ns: int | None = None,
    ) -> ProcessingEvent[PredictionT]:
        if self._is_recently_finalized(frame.inspection_id):
            return ProcessingEvent(
                ProcessingState.FINALIZED,
                frame.inspection_id,
                frame.apple_id,
                0,
                frame.total_frames,
            )
        acceptance = self._store.accept(frame)
        self._touch(frame.inspection_id, wall_time_ns)
        if not acceptance.is_new_frame:
            return self._event(ProcessingState.DUPLICATE, acceptance.session)
        return self._maybe_predict(acceptance.session, simulation_time_ns)

    def handle_completion(
        self,
        completion: InspectionCompletion,
        simulation_time_ns: int,
        wall_time_ns: int | None = None,
    ) -> ProcessingEvent[PredictionT]:
        if self._is_recently_finalized(completion.inspection_id):
            return ProcessingEvent(
                ProcessingState.FINALIZED,
                completion.inspection_id,
                completion.apple_id,
                0,
                completion.total_frames,
                deadline_time_ns=completion.deadline_time_ns,
            )
        session = self._store.complete(completion)
        self._touch(completion.inspection_id, wall_time_ns)
        return self._maybe_predict(session, simulation_time_ns)

    def _maybe_predict(
        self,
        session: InspectionSession,
        simulation_time_ns: int,
    ) -> ProcessingEvent[PredictionT]:
        if session.completion is None:
            return self._event(ProcessingState.BUFFERING, session)
        if session.deadline_reached(simulation_time_ns):
            return self._event(ProcessingState.TIMEOUT, session)
        if not session.has_all_declared_frames:
            return self._event(ProcessingState.BUFFERING, session)
        try:
            predictions = predict_declared_frames(session, self._predictor)
        except PredictorNotConfigured:
            return self._event(ProcessingState.PREDICTOR_UNAVAILABLE, session)
        return self._event(ProcessingState.PREDICTED, session, predictions)

    def expired(self, simulation_time_ns: int) -> tuple[ProcessingEvent[PredictionT], ...]:
        return tuple(
            self._event(ProcessingState.TIMEOUT, session)
            for session in self._store.sessions
            if session.completion is not None
            and session.deadline_reached(simulation_time_ns)
        )

    def stale(
        self,
        wall_time_ns: int,
        timeout_ns: int,
    ) -> tuple[ProcessingEvent[PredictionT], ...]:
        return tuple(
            self._event(ProcessingState.STALE, session)
            for session in self._store.sessions
            if session.completion is None
            if wall_time_ns - self._last_wall_activity_ns.get(
                session.inspection_id,
                wall_time_ns,
            ) >= timeout_ns
        )

    def finalize(self, inspection_id: str) -> None:
        if not inspection_id:
            return
        self._store.pop(inspection_id)
        self._last_wall_activity_ns.pop(inspection_id, None)
        if inspection_id in self._recent_finalized_set:
            return
        if len(self._recent_finalized) == self._recent_finalized.maxlen:
            expired = self._recent_finalized.popleft()
            self._recent_finalized_set.discard(expired)
        self._recent_finalized.append(inspection_id)
        self._recent_finalized_set.add(inspection_id)


def _reliable_qos(depth: int) -> Any:
    if QoSProfile is None:
        raise RuntimeError("rclpy is required to construct QoS profiles")
    return QoSProfile(
        reliability=ReliabilityPolicy.RELIABLE,
        durability=DurabilityPolicy.VOLATILE,
        history=HistoryPolicy.KEEP_LAST,
        depth=depth,
    )


def make_input_qos() -> Any:
    return _reliable_qos(INPUT_QOS_DEPTH)


def make_completion_qos() -> Any:
    return _reliable_qos(COMPLETION_QOS_DEPTH)


def make_result_qos() -> Any:
    return _reliable_qos(RESULT_QOS_DEPTH)


class QualityInspectionNode(Node):  # type: ignore[misc]
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
            ("stale_session_timeout_sec", DEFAULT_STALE_SESSION_TIMEOUT_SEC),
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
        self._stale_timeout_ns = int(
            float(self.get_parameter("stale_session_timeout_sec").value) * 1_000_000_000
        )
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
        self._completion_subscription = self.create_subscription(
            InspectionCompleted,
            COMPLETION_TOPIC,
            self._on_inspection_completed,
            make_completion_qos(),
        )
        self._deadline_timer = self.create_timer(
            0.05,
            self._on_deadline_timer,
            clock=self.get_clock(),
        )
        self._steady_clock = Clock(clock_type=ClockType.STEADY_TIME)
        self._stale_timer = self.create_timer(
            0.5,
            self._on_stale_timer,
            clock=self._steady_clock,
        )
        self.get_logger().info(
            f"GPU PC 2 quality node ready: {INPUT_TOPIC} + {COMPLETION_TOPIC} "
            f"-> {OUTPUT_TOPIC}; use_sim_time=true"
        )

    def _simulation_time_ns(self) -> int:
        return int(self.get_clock().now().nanoseconds)

    def _on_inspection_image(self, message: Any) -> None:
        try:
            frame = inspection_frame_from_message(message)
            event = self._coordinator.handle_frame(
                frame,
                self._simulation_time_ns(),
            )
        except InspectionContractError as exc:
            self.get_logger().error(f"Rejected InspectionImage contract: {exc}")
            return
        except Exception as exc:
            self._coordinator.finalize(str(getattr(message, "inspection_id", "")))
            self.get_logger().error(f"Inspection input failed: {exc}")
            return
        self._handle_event(event)

    def _on_inspection_completed(self, message: Any) -> None:
        try:
            completion = inspection_completion_from_message(message)
            event = self._coordinator.handle_completion(
                completion,
                self._simulation_time_ns(),
            )
        except InspectionContractError as exc:
            self.get_logger().error(f"Rejected InspectionCompleted contract: {exc}")
            return
        except Exception as exc:
            self._coordinator.finalize(str(getattr(message, "inspection_id", "")))
            self.get_logger().error(f"Inspection completion failed: {exc}")
            return
        self._handle_event(event)

    def _handle_event(self, event: ProcessingEvent[Any]) -> None:
        if event.state is ProcessingState.BUFFERING:
            self.get_logger().debug(
                f"Buffering {event.inspection_id}: "
                f"{event.received_count}/{event.total_frames} frames"
            )
            return
        if event.state in (ProcessingState.DUPLICATE, ProcessingState.FINALIZED):
            self.get_logger().warning(
                f"Ignored duplicate/finalized input for inspection {event.inspection_id}"
            )
            return
        if event.state is ProcessingState.PREDICTOR_UNAVAILABLE:
            session = self._coordinator.store.get(event.inspection_id)
            frame_indices = session.frame_indices if session is not None else ()
            result = CoreQualityResult(
                None,
                ResultStatus.UNCLASSIFIED,
                None,
                None,
                frame_indices,
            )
            self._publish_result(event, result)
            self._coordinator.finalize(event.inspection_id)
            return
        if event.state is ProcessingState.TIMEOUT:
            self._publish_timeout(event)
            return
        if event.state is ProcessingState.STALE:
            self.get_logger().warning(
                f"Dropped stale inspection without completion: {event.inspection_id}"
            )
            self._coordinator.finalize(event.inspection_id)
            return
        if event.state is ProcessingState.PREDICTED:
            self._finalize_predictions(event)

    def _finalize_predictions(self, event: ProcessingEvent[Any]) -> None:
        session = self._coordinator.store.get(event.inspection_id)
        if session is None:
            return
        measurements = []
        indices = []
        for indexed in event.predictions:
            frame = next(
                item for item in session.ordered_frames
                if item.frame_index == indexed.frame_index
            )
            try:
                measurements.append(
                    combine_prediction_with_geometry(frame, indexed.value)
                )
                indices.append(indexed.frame_index)
            except GeometryMeasurementError as exc:
                self.get_logger().warning(
                    f"Rejected geometry frame {indexed.frame_index} "
                    f"for {event.inspection_id}: {exc}"
                )

        if (
            event.deadline_time_ns is not None
            and self._simulation_time_ns() >= event.deadline_time_ns
        ):
            self.get_logger().warning(
                f"Late computation discarded for {event.inspection_id}"
            )
            self._publish_timeout(event)
            return

        result = aggregate_measurement_frames(
            measurements,
            indices,
            confidence_threshold=self._confidence_threshold,
        )
        self._publish_result(event, result)
        self._coordinator.finalize(event.inspection_id)

    def _publish_timeout(self, event: ProcessingEvent[Any]) -> None:
        result = CoreQualityResult(
            None,
            ResultStatus.TIMEOUT,
            None,
            None,
            (),
        )
        self._publish_result(event, result)
        self._coordinator.finalize(event.inspection_id)

    def _on_deadline_timer(self) -> None:
        for event in self._coordinator.expired(self._simulation_time_ns()):
            self._handle_event(event)

    def _on_stale_timer(self) -> None:
        now_ns = time.monotonic_ns()
        for event in self._coordinator.stale(now_ns, self._stale_timeout_ns):
            self._handle_event(event)

    def _publish_result(self, event: ProcessingEvent[Any], result: CoreQualityResult) -> None:
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
        message.confidence = (
            float(result.confidence) if result.confidence is not None else float("nan")
        )
        measurements = result.measurements
        message.color_ratio = (
            float(measurements.color_ratio) if measurements else float("nan")
        )
        message.diameter_mm = (
            float(measurements.diameter_mm) if measurements else float("nan")
        )
        message.damage_area_cm2 = (
            float(measurements.damage_area_cm2) if measurements else float("nan")
        )
        message.frames_used = len(result.frames_used)
        message.frame_indices = list(result.frames_used)
        message.result_timestamp = now
        message.status = int(getattr(QualityResultMessage, result.status.value))
        self._result_publisher.publish(message)
        self.get_logger().info(
            f"Published {result.status.value} for {event.inspection_id}: "
            f"grade={result.grade.value if result.grade else 'NONE'}, "
            f"frames={list(result.frames_used)}"
        )


def main(args: list[str] | None = None) -> None:
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
