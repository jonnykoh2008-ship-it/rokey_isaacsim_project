import pytest

from appleproj_personal_pc2.pusher_selection import (
    PusherTarget,
    SelectionRegistry,
    decide_pusher,
)


@pytest.mark.parametrize(
    ("grade", "target"),
    [
        ("HIGH", PusherTarget.HIGH_GRADE),
        ("MEDIUM", PusherTarget.MEDIUM_GRADE),
        ("LOW", PusherTarget.LOW_GRADE),
    ],
)
def test_valid_result_selects_semantic_target(grade, target):
    decision = decide_pusher(
        inspection_id="inspection_1",
        apple_id="apple_1",
        grade=grade,
        status="VALID",
    )

    assert decision.target is target
    assert decision.reason == "SELECTED"


@pytest.mark.parametrize(
    "status",
    [
        "RECHECK",
        "UNCLASSIFIED",
        "TIMEOUT",
        "LATE_RESULT",
        "ID_MISMATCH",
        "INSUFFICIENT_VIEWS",
    ],
)
def test_non_valid_result_passes_without_pusher(status):
    decision = decide_pusher(
        inspection_id="inspection_1",
        apple_id="apple_1",
        grade="HIGH",
        status=status,
    )

    assert decision.target is None
    assert decision.reason == f"PASS_THROUGH_STATUS:{status}"


def test_unknown_grade_is_not_selected():
    decision = decide_pusher(
        inspection_id="inspection_1",
        apple_id="apple_1",
        grade="UNKNOWN",
        status="VALID",
    )

    assert decision.target is None
    assert decision.reason == "UNKNOWN_GRADE:UNKNOWN"


def test_registry_marks_duplicate_and_rejects_conflict():
    registry = SelectionRegistry()
    original = registry.register(
        inspection_id="inspection_1",
        apple_id="apple_1",
        grade="HIGH",
        status="VALID",
    )
    duplicate = registry.register(
        inspection_id="inspection_1",
        apple_id="apple_1",
        grade="HIGH",
        status="VALID",
    )

    assert not original.duplicate
    assert duplicate.duplicate

    with pytest.raises(ValueError, match="conflicting result"):
        registry.register(
            inspection_id="inspection_1",
            apple_id="apple_1",
            grade="LOW",
            status="VALID",
        )
