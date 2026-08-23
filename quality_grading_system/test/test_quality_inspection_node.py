from __future__ import annotations

import unittest
from types import SimpleNamespace

from inspection_session import InspectionContractError, InspectionFrame
from quality_inspection_node import (
    DEFAULT_CONFIDENCE_THRESHOLD,
    INPUT_QOS_DEPTH,
    INPUT_TOPIC,
    OUTPUT_TOPIC,
    RESULT_QOS_DEPTH,
    InspectionCoordinator,
    ProcessingState,
    inspection_frame_from_message,
)


def make_message(
    frame_index: int,
    *,
    total_frames: int = 2,
    inspection_id: str = "inspection-ros-001",
    apple_id: str = "apple-ros-001",
) -> SimpleNamespace:
    return SimpleNamespace(
        inspection_id=inspection_id,
        apple_id=apple_id,
        frame_index=frame_index,
        total_frames=total_frames,
        image=SimpleNamespace(data=bytearray(f"jpeg-{frame_index}".encode()), format="jpeg"),
    )


class MessageAdapterTest(unittest.TestCase):
    def test_converts_a_ros_like_message_without_requiring_ros_imports(self) -> None:
        frame = inspection_frame_from_message(make_message(1))

        self.assertEqual(frame.inspection_id, "inspection-ros-001")
        self.assertEqual(frame.apple_id, "apple-ros-001")
        self.assertEqual(frame.frame_index, 1)
        self.assertEqual(frame.total_frames, 2)
        self.assertEqual(frame.image_data, b"jpeg-1")
        self.assertEqual(frame.image_format, "jpeg")

    def test_invalid_message_content_is_rejected_by_the_core_contract(self) -> None:
        message = make_message(0)
        message.image.data = bytearray()

        with self.assertRaises(InspectionContractError):
            inspection_frame_from_message(message)

    def test_rejects_mismatched_outer_and_compressed_image_headers(self) -> None:
        message = make_message(0)
        message.header = SimpleNamespace(
            stamp=SimpleNamespace(sec=10, nanosec=20),
            frame_id="camera",
        )
        message.image.header = SimpleNamespace(
            stamp=SimpleNamespace(sec=10, nanosec=21),
            frame_id="camera",
        )

        with self.assertRaises(InspectionContractError):
            inspection_frame_from_message(message)


class CoordinatorTest(unittest.TestCase):
    def test_buffers_until_all_declared_frames_are_received(self) -> None:
        class IndexPredictor:
            def predict(self, frame: InspectionFrame) -> str:
                return f"prediction-{frame.frame_index}"

        coordinator = InspectionCoordinator(IndexPredictor())

        first = coordinator.handle(inspection_frame_from_message(make_message(1)))
        complete = coordinator.handle(inspection_frame_from_message(make_message(0)))

        self.assertEqual(first.state, ProcessingState.BUFFERING)
        self.assertEqual(complete.state, ProcessingState.PREDICTED)
        self.assertEqual(
            tuple(item.value for item in complete.predictions),
            ("prediction-0", "prediction-1"),
        )

    def test_duplicate_message_does_not_repeat_inference(self) -> None:
        calls: list[int] = []

        class RecordingPredictor:
            def predict(self, frame: InspectionFrame) -> int:
                calls.append(frame.frame_index)
                return frame.frame_index

        coordinator = InspectionCoordinator(RecordingPredictor())
        first = inspection_frame_from_message(make_message(0, total_frames=1))

        complete = coordinator.handle(first)
        duplicate = coordinator.handle(first)

        self.assertEqual(complete.state, ProcessingState.PREDICTED)
        self.assertEqual(duplicate.state, ProcessingState.DUPLICATE)
        self.assertEqual(calls, [0])

    def test_unconfigured_model_produces_no_predictions(self) -> None:
        from predictor import UnconfiguredPredictor

        coordinator = InspectionCoordinator(UnconfiguredPredictor())
        event = coordinator.handle(
            inspection_frame_from_message(make_message(0, total_frames=1))
        )

        self.assertEqual(event.state, ProcessingState.PREDICTOR_UNAVAILABLE)
        self.assertEqual(event.predictions, ())


class TemporaryRosContractTest(unittest.TestCase):
    def test_approved_topic_names_and_result_queue_depth(self) -> None:
        self.assertEqual(INPUT_TOPIC, "/quality/inspection_images")
        self.assertEqual(OUTPUT_TOPIC, "/quality/results")
        self.assertEqual(RESULT_QOS_DEPTH, 10)
        self.assertEqual(INPUT_QOS_DEPTH, 6)
        self.assertEqual(DEFAULT_CONFIDENCE_THRESHOLD, 0.5)


if __name__ == "__main__":
    unittest.main()
