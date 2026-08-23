"""Pure-Python quality labels shared by the demo and synthetic dataset tools.

The thresholds intentionally mirror ``docs/features/quality_grading.md``.
Model confidence remains configurable around the decided initial threshold so
it can be calibrated after validation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Iterable


class Grade(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ResultStatus(str, Enum):
    VALID = "VALID"
    RECHECK = "RECHECK"
    UNCLASSIFIED = "UNCLASSIFIED"
    TIMEOUT = "TIMEOUT"
    LATE_RESULT = "LATE_RESULT"
    ID_MISMATCH = "ID_MISMATCH"
    INSUFFICIENT_VIEWS = "INSUFFICIENT_VIEWS"


@dataclass(frozen=True)
class AppleMeasurements:
    color_ratio: float
    diameter_mm: float
    damage_area_cm2: float
    severe_defect: bool = False


@dataclass(frozen=True)
class QualityResult:
    grade: str | None
    status: str
    confidence: float | None
    measurements: AppleMeasurements | None
    frames_used: tuple[int, ...]

    def to_dict(self) -> dict:
        value = asdict(self)
        value["frames_used"] = list(self.frames_used)
        return value


@dataclass(frozen=True)
class FrameMeasurements:
    """One frame's model/geometric outputs and their validity confidence.

    ``None`` means the measurement was not produced.  This is important for
    the current synthetic dataset: diameter labels exist, while color and
    damage annotations do not.
    """

    color_ratio: float | None = None
    diameter_mm: float | None = None
    damage_area_cm2: float | None = None
    severe_defect: bool | None = None
    color_confidence: float | None = None
    diameter_confidence: float | None = None
    damage_confidence: float | None = None
    severe_confidence: float | None = None

    @property
    def confidence(self) -> float | None:
        values = [
            value
            for value in (
                self.color_confidence,
                self.diameter_confidence,
                self.damage_confidence,
                self.severe_confidence,
            )
            if value is not None
        ]
        return sum(values) / len(values) if values else None


def grade_measurements(measurements: AppleMeasurements) -> Grade:
    """Apply the documented HIGH / MEDIUM / LOW product rules."""
    if (
        measurements.color_ratio < 0.60
        or measurements.diameter_mm < 60.0
        or measurements.damage_area_cm2 > 2.5
        or measurements.severe_defect
    ):
        return Grade.LOW
    if (
        measurements.color_ratio >= 0.80
        and measurements.diameter_mm >= 75.0
        and measurements.damage_area_cm2 <= 1.0
        and not measurements.severe_defect
    ):
        return Grade.HIGH
    return Grade.MEDIUM


def aggregate_frames(
    frame_measurements: Iterable[AppleMeasurements],
    frame_indices: Iterable[int],
    *,
    min_valid_views: int = 4,
    confidence: float | None = None,
) -> QualityResult:
    """Aggregate representative views conservatively for a single apple.

    Color uses the mean, diameter the median, damage the maximum computable
    view, and severe defect a conservative ``any`` rule.  Callers provide the
    representative frame indices selected by GPU PC 1.
    """
    values = list(frame_measurements)
    indices = tuple(frame_indices)
    if len(values) != len(indices):
        raise ValueError("frame_measurements and frame_indices must have equal length")
    if len(values) < min_valid_views:
        fallback = values[0] if values else None
        return QualityResult(None, ResultStatus.INSUFFICIENT_VIEWS, confidence, fallback, indices)

    ordered_diameter = sorted(item.diameter_mm for item in values)
    middle = len(values) // 2
    measurements = AppleMeasurements(
        color_ratio=sum(item.color_ratio for item in values) / len(values),
        diameter_mm=ordered_diameter[middle],
        damage_area_cm2=max(item.damage_area_cm2 for item in values),
        severe_defect=any(item.severe_defect for item in values),
    )
    return QualityResult(grade_measurements(measurements), ResultStatus.VALID, confidence, measurements, indices)


def _is_valid(value: object | None, confidence: float | None, threshold: float) -> bool:
    return value is not None and confidence is not None and confidence >= threshold


def aggregate_measurement_frames(
    frame_measurements: Iterable[FrameMeasurements],
    frame_indices: Iterable[int],
    *,
    confidence_threshold: float = 0.5,
    min_valid_views: int = 4,
    min_damage_views: int = 2,
) -> QualityResult:
    """Aggregate model measurements using the decided GPU PC 2 policy."""

    values = list(frame_measurements)
    indices = tuple(frame_indices)
    if len(values) != len(indices):
        raise ValueError("frame_measurements and frame_indices must have equal length")
    if not 0.0 <= confidence_threshold <= 1.0:
        raise ValueError("confidence_threshold must be between 0 and 1")

    required_fields = ("color_ratio", "diameter_mm", "damage_area_cm2", "severe_defect")
    if values and any(all(getattr(item, field) is None for item in values) for field in required_fields):
        return QualityResult(None, ResultStatus.UNCLASSIFIED, None, None, indices)

    valid_pairs = [
        (index, item)
        for index, item in zip(indices, values)
        if _is_valid(item.color_ratio, item.color_confidence, confidence_threshold)
        and _is_valid(item.diameter_mm, item.diameter_confidence, confidence_threshold)
        and _is_valid(item.severe_defect, item.severe_confidence, confidence_threshold)
    ]
    used_indices = tuple(index for index, _ in valid_pairs)
    valid_confidences = [
        item.confidence
        for _, item in valid_pairs
        if item.confidence is not None
    ]
    final_confidence = (
        sum(valid_confidences) / len(valid_confidences)
        if valid_confidences
        else None
    )

    if len(valid_pairs) < min_valid_views:
        return QualityResult(
            None,
            ResultStatus.INSUFFICIENT_VIEWS,
            final_confidence,
            None,
            used_indices,
        )

    damage_values = [
        item.damage_area_cm2
        for _, item in valid_pairs
        if _is_valid(item.damage_area_cm2, item.damage_confidence, confidence_threshold)
    ]
    if len(damage_values) < min_damage_views:
        return QualityResult(
            None,
            ResultStatus.RECHECK,
            final_confidence,
            None,
            used_indices,
        )

    colors = [item.color_ratio for _, item in valid_pairs]
    diameters = sorted(item.diameter_mm for _, item in valid_pairs)
    assert all(value is not None for value in colors)
    assert all(value is not None for value in diameters)
    measurements = AppleMeasurements(
        color_ratio=sum(float(value) for value in colors) / len(colors),
        diameter_mm=float(diameters[len(diameters) // 2]),
        damage_area_cm2=max(float(value) for value in damage_values if value is not None),
        severe_defect=any(bool(item.severe_defect) for _, item in valid_pairs),
    )
    return QualityResult(
        grade_measurements(measurements),
        ResultStatus.VALID,
        final_confidence,
        measurements,
        used_indices,
    )
