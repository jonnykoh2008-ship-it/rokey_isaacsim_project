"""ROS-independent aggregation for Personal PC 2 quality-result displays."""

from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class LatestResult:
    """Latest accepted result for one apple."""

    inspection_id: str
    grade: str
    status: str


@dataclass(frozen=True)
class ResultSummarySnapshot:
    """Copy of the current summary suitable for display or serialization."""

    total_messages: int
    unique_inspections: int
    duplicate_messages: int
    grade_counts: dict[str, int]
    status_counts: dict[str, int]
    latest_by_apple: dict[str, LatestResult]


class ResultSummary:
    """Count quality results without depending on generated ROS message types."""

    def __init__(self) -> None:
        self._total_messages = 0
        self._duplicate_messages = 0
        self._inspection_to_apple: dict[str, str] = {}
        self._grade_counts: Counter[str] = Counter()
        self._status_counts: Counter[str] = Counter()
        self._latest_by_apple: dict[str, LatestResult] = {}

    def record(
        self,
        *,
        inspection_id: str,
        apple_id: str,
        grade: str,
        status: str,
    ) -> bool:
        """Record a result and return ``True`` only for a new inspection."""

        values = {
            "inspection_id": inspection_id,
            "apple_id": apple_id,
            "grade": grade,
            "status": status,
        }
        for field_name, value in values.items():
            if not value.strip():
                raise ValueError(f"{field_name} must not be empty")

        known_apple = self._inspection_to_apple.get(inspection_id)
        if known_apple is not None and known_apple != apple_id:
            raise ValueError(
                f"inspection_id {inspection_id} changed apple_id "
                f"from {known_apple} to {apple_id}"
            )

        self._total_messages += 1
        if known_apple is not None:
            self._duplicate_messages += 1
            return False

        self._inspection_to_apple[inspection_id] = apple_id
        self._grade_counts[grade] += 1
        self._status_counts[status] += 1
        self._latest_by_apple[apple_id] = LatestResult(
            inspection_id=inspection_id,
            grade=grade,
            status=status,
        )
        return True

    def snapshot(self) -> ResultSummarySnapshot:
        """Return detached copies so callers cannot mutate internal state."""

        return ResultSummarySnapshot(
            total_messages=self._total_messages,
            unique_inspections=len(self._inspection_to_apple),
            duplicate_messages=self._duplicate_messages,
            grade_counts=dict(self._grade_counts),
            status_counts=dict(self._status_counts),
            latest_by_apple=dict(self._latest_by_apple),
        )
