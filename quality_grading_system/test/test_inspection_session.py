from __future__ import annotations

import unittest

from inspection_session import (
    DuplicateFrameConflict,
    InspectionContractError,
    InspectionFrame,
    InspectionCompletion,
    InspectionIdentityMismatch,
    InspectionStore,
    RESULT_DEADLINE_NS,
    TotalFramesMismatch,
)
from predictor import (
    IncompleteInspectionError,
    PredictorNotConfigured,
    UnconfiguredPredictor,
    predict_declared_frames,
)


def make_frame(
    frame_index: int,
    *,
    inspection_id: str = "inspection-001",
    apple_id: str = "apple-001",
    total_frames: int = 3,
    image_data: bytes | None = None,
) -> InspectionFrame:
    return InspectionFrame(
        inspection_id=inspection_id,
        apple_id=apple_id,
        frame_index=frame_index,
        total_frames=total_frames,
        image_data=image_data if image_data is not None else f"jpeg-{frame_index}".encode(),
        image_format="jpeg",
    )


class InspectionStoreTest(unittest.TestCase):
    def test_accepts_out_of_order_frames_and_returns_them_sorted(self) -> None:
        store = InspectionStore()

        for index in (2, 0, 1):
            acceptance = store.accept(make_frame(index))
            self.assertTrue(acceptance.is_new_frame)

        session = store.get("inspection-001")
        self.assertIsNotNone(session)
        assert session is not None
        self.assertTrue(session.has_all_declared_frames)
        self.assertEqual(session.received_count, 3)
        self.assertEqual(session.frame_indices, (0, 1, 2))

    def test_identical_duplicate_is_idempotent(self) -> None:
        store = InspectionStore()
        frame = make_frame(0)

        self.assertTrue(store.accept(frame).is_new_frame)
        self.assertFalse(store.accept(frame).is_new_frame)
        self.assertEqual(store.get(frame.inspection_id).received_count, 1)  # type: ignore[union-attr]

    def test_conflicting_duplicate_is_rejected(self) -> None:
        store = InspectionStore()
        store.accept(make_frame(0, image_data=b"first"))

        with self.assertRaises(DuplicateFrameConflict):
            store.accept(make_frame(0, image_data=b"different"))

    def test_apple_id_cannot_change_within_an_inspection(self) -> None:
        store = InspectionStore()
        store.accept(make_frame(0))

        with self.assertRaises(InspectionIdentityMismatch):
            store.accept(make_frame(1, apple_id="apple-002"))

    def test_total_frames_cannot_change_within_an_inspection(self) -> None:
        store = InspectionStore()
        store.accept(make_frame(0))

        with self.assertRaises(TotalFramesMismatch):
            store.accept(make_frame(1, total_frames=4))

    def test_rejects_more_unique_frames_than_declared(self) -> None:
        store = InspectionStore()
        store.accept(make_frame(10, total_frames=1))

        with self.assertRaises(InspectionContractError):
            store.accept(make_frame(11, total_frames=1))

    def test_frame_validation_does_not_assume_zero_or_one_based_indices(self) -> None:
        self.assertEqual(make_frame(0).frame_index, 0)
        self.assertEqual(make_frame(3).frame_index, 3)

    def test_rejects_invalid_required_fields(self) -> None:
        with self.assertRaises(InspectionContractError):
            make_frame(0, inspection_id="")
        with self.assertRaises(InspectionContractError):
            make_frame(0, apple_id="")
        with self.assertRaises(InspectionContractError):
            make_frame(0, total_frames=7)
        with self.assertRaises(InspectionContractError):
            make_frame(0, image_data=b"")

    def test_store_pop_leaves_lifecycle_decision_to_the_caller(self) -> None:
        store = InspectionStore()
        store.accept(make_frame(0))

        removed = store.pop("inspection-001")

        self.assertIsNotNone(removed)
        self.assertIsNone(store.get("inspection-001"))
        self.assertEqual(len(store), 0)

    def test_completion_event_can_arrive_before_frames_and_uses_sim_deadline(self) -> None:
        store = InspectionStore()
        completion = InspectionCompletion(
            "inspection-early-complete",
            "apple-001",
            4,
            10_000_000_000,
        )
        session = store.complete(completion)

        self.assertFalse(session.deadline_reached(completion.deadline_time_ns - 1))
        self.assertTrue(session.deadline_reached(completion.deadline_time_ns))
        self.assertEqual(
            completion.deadline_time_ns,
            completion.roi_exit_time_ns + RESULT_DEADLINE_NS,
        )
        accepted = store.accept(
            make_frame(
                0,
                inspection_id=completion.inspection_id,
                apple_id=completion.apple_id,
                total_frames=completion.total_frames,
            )
        )
        self.assertTrue(accepted.is_new_frame)

    def test_completion_identity_must_match_existing_session(self) -> None:
        store = InspectionStore()
        store.accept(make_frame(0))

        with self.assertRaises(InspectionIdentityMismatch):
            store.complete(InspectionCompletion("inspection-001", "apple-other", 3, 1))


class PredictorBoundaryTest(unittest.TestCase):
    def test_fake_predictor_runs_in_frame_index_order(self) -> None:
        store = InspectionStore()
        for index in (2, 0, 1):
            session = store.accept(make_frame(index)).session

        class ByteCountPredictor:
            def predict(self, frame: InspectionFrame) -> int:
                return len(frame.image_data)

        predictions = predict_declared_frames(session, ByteCountPredictor())

        self.assertEqual(tuple(item.frame_index for item in predictions), (0, 1, 2))
        self.assertEqual(tuple(item.value for item in predictions), (6, 6, 6))

    def test_inference_rejects_an_incomplete_declared_batch(self) -> None:
        session = InspectionStore().accept(make_frame(0)).session

        with self.assertRaises(IncompleteInspectionError):
            predict_declared_frames(session, UnconfiguredPredictor())

    def test_unconfigured_predictor_never_fabricates_a_result(self) -> None:
        store = InspectionStore()
        session = None
        for index in range(3):
            session = store.accept(make_frame(index)).session
        assert session is not None

        with self.assertRaises(PredictorNotConfigured):
            predict_declared_frames(session, UnconfiguredPredictor())


if __name__ == "__main__":
    unittest.main()
