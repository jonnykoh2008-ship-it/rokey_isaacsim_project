"""Transport-independent phase-2 pusher selection for Personal PC 2."""

from dataclasses import dataclass, replace
from enum import Enum


class PusherTarget(str, Enum):
    """Semantic target; final shared ``pusher_id`` values remain TBD."""

    HIGH_GRADE = "HIGH_GRADE"
    MEDIUM_GRADE = "MEDIUM_GRADE"
    LOW_GRADE = "LOW_GRADE"


@dataclass(frozen=True)
class SelectionDecision:
    inspection_id: str
    apple_id: str
    grade: str
    status: str
    target: PusherTarget | None
    reason: str
    duplicate: bool = False


GRADE_TARGETS = {
    "HIGH": PusherTarget.HIGH_GRADE,
    "MEDIUM": PusherTarget.MEDIUM_GRADE,
    "LOW": PusherTarget.LOW_GRADE,
}


def decide_pusher(
    *,
    inspection_id: str,
    apple_id: str,
    grade: str,
    status: str,
) -> SelectionDecision:
    """Select a semantic pusher target without creating a SortCommand."""

    for field_name, value in (
        ("inspection_id", inspection_id),
        ("apple_id", apple_id),
        ("grade", grade),
        ("status", status),
    ):
        if not value.strip():
            raise ValueError(f"{field_name} must not be empty")

    if status != "VALID":
        return SelectionDecision(
            inspection_id=inspection_id,
            apple_id=apple_id,
            grade=grade,
            status=status,
            target=None,
            reason=f"PASS_THROUGH_STATUS:{status}",
        )

    target = GRADE_TARGETS.get(grade)
    if target is None:
        return SelectionDecision(
            inspection_id=inspection_id,
            apple_id=apple_id,
            grade=grade,
            status=status,
            target=None,
            reason=f"UNKNOWN_GRADE:{grade}",
        )

    return SelectionDecision(
        inspection_id=inspection_id,
        apple_id=apple_id,
        grade=grade,
        status=status,
        target=target,
        reason="SELECTED",
    )


class SelectionRegistry:
    """Detect duplicate or conflicting decisions for an inspection."""

    def __init__(self) -> None:
        self._decisions: dict[str, SelectionDecision] = {}

    def register(
        self,
        *,
        inspection_id: str,
        apple_id: str,
        grade: str,
        status: str,
    ) -> SelectionDecision:
        decision = decide_pusher(
            inspection_id=inspection_id,
            apple_id=apple_id,
            grade=grade,
            status=status,
        )
        known = self._decisions.get(inspection_id)
        if known is None:
            self._decisions[inspection_id] = decision
            return decision
        if (
            known.apple_id != decision.apple_id
            or known.grade != decision.grade
            or known.status != decision.status
        ):
            raise ValueError(
                f"conflicting result for inspection_id {inspection_id}"
            )
        return replace(known, duplicate=True)
