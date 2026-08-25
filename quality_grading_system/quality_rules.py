"""Pure-Python quality labels shared by the demo and synthetic dataset tools.

The thresholds intentionally mirror ``docs/features/quality_grading.md``.
Model confidence remains configurable around the decided initial threshold so
it can be calibrated after validation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from statistics import median
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
    color_ratio: float | None = None
    diameter_mm: float | None = None
    damage_area_cm2: float | None = None
    severe_defect: bool | None = None


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


def grade_diameter_mm(diameter_mm: float) -> Grade:
    """Apply the approved size-only MVP boundaries."""
    if diameter_mm < 0.0:
        raise ValueError("diameter_mm must be non-negative")
    if diameter_mm < 60.0:
        return Grade.LOW
    if diameter_mm >= 75.0:
        return Grade.HIGH
    return Grade.MEDIUM


def grade_measurements(measurements: AppleMeasurements) -> Grade:
    """Grade only by diameter during the current OpenCV MVP."""
    if measurements.diameter_mm is None:
        raise ValueError("diameter_mm is required for size-only grading")
    return grade_diameter_mm(measurements.diameter_mm)


def aggregate_frames(
    frame_measurements: Iterable[AppleMeasurements],
    frame_indices: Iterable[int],
    *,
    min_valid_views: int = 1,
    confidence: float | None = None,
) -> QualityResult:
    """Aggregate size measurements for one apple using the diameter median."""
    values = list(frame_measurements)
    indices = tuple(frame_indices)
    if len(values) != len(indices):
        raise ValueError("frame_measurements and frame_indices must have equal length")
    if len(values) < min_valid_views:
        fallback = values[0] if values else None
        return QualityResult(None, ResultStatus.INSUFFICIENT_VIEWS, confidence, fallback, indices)

    diameters = [item.diameter_mm for item in values]
    if any(value is None for value in diameters):
        return QualityResult(
            None,
            ResultStatus.UNCLASSIFIED,
            confidence,
            None,
            indices,
        )
    measurements = AppleMeasurements(
        diameter_mm=float(
            median(float(value) for value in diameters if value is not None)
        ),
    )
    return QualityResult(grade_measurements(measurements), ResultStatus.VALID, confidence, measurements, indices)


def _is_valid(value: object | None, confidence: float | None, threshold: float) -> bool:
    return value is not None and confidence is not None and confidence >= threshold


def aggregate_measurement_frames(
    frame_measurements: Iterable[FrameMeasurements],
    frame_indices: Iterable[int],
    *,
    confidence_threshold: float = 0.5,
    min_valid_views: int = 1,
    min_damage_views: int = 0,
) -> QualityResult:
    """Aggregate model measurements using the decided GPU PC 2 policy."""

    values = list(frame_measurements)
    indices = tuple(frame_indices)
    if len(values) != len(indices):
        raise ValueError("frame_measurements and frame_indices must have equal length")
    if not 0.0 <= confidence_threshold <= 1.0:
        raise ValueError("confidence_threshold must be between 0 and 1")

    del min_damage_views
    if values and all(item.diameter_mm is None for item in values):
        return QualityResult(None, ResultStatus.UNCLASSIFIED, None, None, indices)

    valid_pairs = [
        (index, item)
        for index, item in zip(indices, values)
        if _is_valid(
            item.diameter_mm,
            item.diameter_confidence,
            confidence_threshold,
        )
    ]
    used_indices = tuple(index for index, _ in valid_pairs)
    valid_confidences = [
        item.diameter_confidence
        for _, item in valid_pairs
        if item.diameter_confidence is not None
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

    diameters = [item.diameter_mm for _, item in valid_pairs]
    assert all(value is not None for value in diameters)
    measurements = AppleMeasurements(
        diameter_mm=float(
            median(float(value) for value in diameters if value is not None)
        ),
    )
    return QualityResult(
        grade_measurements(measurements),
        ResultStatus.VALID,
        final_confidence,
        measurements,
        used_indices,
    )
