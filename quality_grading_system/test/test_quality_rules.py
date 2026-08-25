from __future__ import annotations

import unittest

from quality_rules import (
    AppleMeasurements,
    FrameMeasurements,
    Grade,
    ResultStatus,
    aggregate_frames,
    aggregate_measurement_frames,
    grade_diameter_mm,
    grade_measurements,
)


class SizeRuleBoundaryTest(unittest.TestCase):
    def test_low_is_strictly_below_60_mm(self) -> None:
        self.assertEqual(grade_diameter_mm(59.999), Grade.LOW)
        self.assertEqual(grade_diameter_mm(60.0), Grade.MEDIUM)

    def test_high_includes_75_mm(self) -> None:
        self.assertEqual(grade_diameter_mm(74.999), Grade.MEDIUM)
        self.assertEqual(grade_diameter_mm(75.0), Grade.HIGH)

    def test_current_mvp_ignores_deferred_quality_fields(self) -> None:
        result = grade_measurements(
            AppleMeasurements(
                color_ratio=0.0,
                diameter_mm=80.0,
                damage_area_cm2=99.0,
                severe_defect=True,
            )
        )
        self.assertEqual(result, Grade.HIGH)

    def test_negative_diameter_is_invalid(self) -> None:
        with self.assertRaises(ValueError):
            grade_diameter_mm(-0.1)


class SizeAggregationTest(unittest.TestCase):
    @staticmethod
    def frame(diameter: float, confidence: float = 0.9) -> FrameMeasurements:
        return FrameMeasurements(
            diameter_mm=diameter,
            diameter_confidence=confidence,
        )

    def test_diameter_only_measurements_produce_valid_result(self) -> None:
        result = aggregate_measurement_frames(
            [self.frame(75.0)],
            [3],
        )
        self.assertEqual(result.status, ResultStatus.VALID)
        self.assertEqual(result.grade, Grade.HIGH)
        self.assertEqual(result.frames_used, (3,))
        self.assertEqual(result.confidence, 0.9)
        assert result.measurements is not None
        self.assertEqual(result.measurements.diameter_mm, 75.0)
        self.assertIsNone(result.measurements.color_ratio)
        self.assertIsNone(result.measurements.damage_area_cm2)

    def test_even_frame_count_uses_statistical_median(self) -> None:
        result = aggregate_measurement_frames(
            [self.frame(value) for value in (59.0, 59.0, 75.0, 75.0)],
            range(4),
            min_valid_views=4,
        )
        self.assertEqual(result.status, ResultStatus.VALID)
        assert result.measurements is not None
        self.assertEqual(result.measurements.diameter_mm, 67.0)
        self.assertEqual(result.grade, Grade.MEDIUM)

    def test_legacy_aggregate_also_uses_statistical_median(self) -> None:
        values = [
            AppleMeasurements(diameter_mm=value)
            for value in (59.0, 59.0, 75.0, 75.0)
        ]
        result = aggregate_frames(values, range(4), min_valid_views=4)
        self.assertEqual(result.status, ResultStatus.VALID)
        assert result.measurements is not None
        self.assertEqual(result.measurements.diameter_mm, 67.0)

    def test_low_confidence_reduces_valid_view_count(self) -> None:
        frames = [self.frame(80.0) for _ in range(4)]
        frames[0] = self.frame(80.0, confidence=0.49)
        result = aggregate_measurement_frames(
            frames,
            range(4),
            confidence_threshold=0.5,
            min_valid_views=4,
        )
        self.assertEqual(result.status, ResultStatus.INSUFFICIENT_VIEWS)

    def test_missing_diameter_is_unclassified(self) -> None:
        result = aggregate_measurement_frames(
            [FrameMeasurements(color_ratio=0.9, color_confidence=0.9)],
            [0],
        )
        self.assertEqual(result.status, ResultStatus.UNCLASSIFIED)
        self.assertIsNone(result.grade)


if __name__ == "__main__":
    unittest.main()
