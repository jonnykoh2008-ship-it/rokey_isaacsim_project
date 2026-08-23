from __future__ import annotations

import unittest

from quality_rules import (
    AppleMeasurements,
    FrameMeasurements,
    Grade,
    ResultStatus,
    aggregate_measurement_frames,
    grade_measurements,
)


def grade(
    color_ratio: float,
    diameter_mm: float,
    damage_area_cm2: float,
    severe_defect: bool = False,
) -> Grade:
    return grade_measurements(
        AppleMeasurements(color_ratio, diameter_mm, damage_area_cm2, severe_defect)
    )


class QualityRuleBoundaryTest(unittest.TestCase):
    def test_high_includes_its_documented_boundaries(self) -> None:
        self.assertEqual(grade(0.80, 75.0, 1.0), Grade.HIGH)

    def test_low_uses_strict_color_and_diameter_lower_bounds(self) -> None:
        self.assertEqual(grade(0.599_999, 80.0, 0.5), Grade.LOW)
        self.assertEqual(grade(0.90, 59.999, 0.5), Grade.LOW)

    def test_low_requires_damage_to_exceed_2_5(self) -> None:
        self.assertEqual(grade(0.70, 70.0, 2.5), Grade.MEDIUM)
        self.assertEqual(grade(0.90, 80.0, 2.500_001), Grade.LOW)

    def test_severe_defect_always_produces_low(self) -> None:
        self.assertEqual(grade(0.95, 85.0, 0.0, severe_defect=True), Grade.LOW)

    def test_medium_covers_sellable_values_between_high_and_low(self) -> None:
        self.assertEqual(grade(0.60, 60.0, 2.5), Grade.MEDIUM)
        self.assertEqual(grade(0.79, 80.0, 0.5), Grade.MEDIUM)
        self.assertEqual(grade(0.90, 80.0, 1.000_001), Grade.MEDIUM)


class MeasurementAggregationTest(unittest.TestCase):
    @staticmethod
    def frame(color: float, diameter: float, damage: float, severe: bool = False):
        return FrameMeasurements(
            color_ratio=color,
            diameter_mm=diameter,
            damage_area_cm2=damage,
            severe_defect=severe,
            color_confidence=0.9,
            diameter_confidence=0.8,
            damage_confidence=0.7,
            severe_confidence=0.9,
        )

    def test_uses_average_median_max_and_any(self) -> None:
        frames = [
            self.frame(0.70, 74.0, 0.2),
            self.frame(0.80, 76.0, 0.4),
            self.frame(0.90, 80.0, 1.2),
            self.frame(0.80, 75.0, 0.3),
        ]
        result = aggregate_measurement_frames(frames, range(4))

        self.assertEqual(result.status, ResultStatus.VALID)
        self.assertEqual(result.grade, Grade.MEDIUM)
        assert result.measurements is not None
        self.assertAlmostEqual(result.measurements.color_ratio, 0.80)
        self.assertEqual(result.measurements.diameter_mm, 76.0)
        self.assertEqual(result.measurements.damage_area_cm2, 1.2)

    def test_missing_dataset_heads_are_unclassified_not_fabricated(self) -> None:
        diameter_only = [
            FrameMeasurements(diameter_mm=75.0, diameter_confidence=0.9)
            for _ in range(4)
        ]
        result = aggregate_measurement_frames(diameter_only, range(4))

        self.assertEqual(result.status, ResultStatus.UNCLASSIFIED)
        self.assertIsNone(result.grade)
        self.assertIsNone(result.measurements)

    def test_low_confidence_reduces_valid_view_count(self) -> None:
        frames = [self.frame(0.85, 80.0, 0.2) for _ in range(4)]
        frames[0] = FrameMeasurements(
            **{
                **frames[0].__dict__,
                "color_confidence": 0.49,
            }
        )
        result = aggregate_measurement_frames(frames, range(4), confidence_threshold=0.5)
        self.assertEqual(result.status, ResultStatus.INSUFFICIENT_VIEWS)


if __name__ == "__main__":
    unittest.main()
