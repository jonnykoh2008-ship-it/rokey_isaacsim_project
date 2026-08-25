import json

import pytest

from appleproj_personal_pc2.event_history import JsonlEventHistory


def test_history_appends_one_json_record(tmp_path):
    history_path = tmp_path / "events.jsonl"
    history = JsonlEventHistory(history_path)

    record = history.append(
        event_type="QUALITY_RESULT",
        simulation_time_ns=123,
        received_wall_time_ns=456,
        payload={"apple_id": "apple_1", "status": "VALID"},
    )

    stored = json.loads(history_path.read_text(encoding="utf-8"))
    assert stored == record
    assert stored["simulation_time_ns"] == 123
    assert stored["received_wall_time_ns"] == 456


def test_history_rejects_negative_simulation_time(tmp_path):
    history = JsonlEventHistory(tmp_path / "events.jsonl")

    with pytest.raises(ValueError, match="must not be negative"):
        history.append(
            event_type="QUALITY_RESULT",
            simulation_time_ns=-1,
            payload={},
        )


def test_history_rejects_empty_path():
    with pytest.raises(ValueError, match="path must not be empty"):
        JsonlEventHistory("")
