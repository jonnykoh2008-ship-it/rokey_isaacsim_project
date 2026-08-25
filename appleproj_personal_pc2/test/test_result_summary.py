import pytest

from appleproj_personal_pc2.result_summary import LatestResult, ResultSummary


def test_summary_counts_unique_and_duplicate_results():
    summary = ResultSummary()

    assert summary.record(
        inspection_id="inspection_1",
        apple_id="apple_1",
        grade="HIGH",
        status="VALID",
    )
    assert not summary.record(
        inspection_id="inspection_1",
        apple_id="apple_1",
        grade="HIGH",
        status="VALID",
    )

    snapshot = summary.snapshot()
    assert snapshot.total_messages == 2
    assert snapshot.unique_inspections == 1
    assert snapshot.duplicate_messages == 1
    assert snapshot.grade_counts == {"HIGH": 1}
    assert snapshot.status_counts == {"VALID": 1}
    assert snapshot.latest_by_apple == {
        "apple_1": LatestResult("inspection_1", "HIGH", "VALID")
    }


def test_summary_rejects_inspection_id_reuse_for_another_apple():
    summary = ResultSummary()
    summary.record(
        inspection_id="inspection_1",
        apple_id="apple_1",
        grade="HIGH",
        status="VALID",
    )

    with pytest.raises(ValueError, match="changed apple_id"):
        summary.record(
            inspection_id="inspection_1",
            apple_id="apple_2",
            grade="LOW",
            status="VALID",
        )


def test_summary_rejects_empty_fields():
    summary = ResultSummary()

    with pytest.raises(ValueError, match="inspection_id"):
        summary.record(
            inspection_id="",
            apple_id="apple_1",
            grade="HIGH",
            status="VALID",
        )
