from appleproj_personal_pc2.monitor_state import ENTER, EXIT, MonitorState


def notice_codes(notices):
    return [notice.code for notice in notices]


def test_checkpoint_exit_starts_deadline_and_expiration_is_one_shot():
    state = MonitorState(
        deadline_ns=500_000_000,
        deadline_checkpoint_id="camera_roi",
    )
    state.process_checkpoint(
        apple_id="apple_1",
        checkpoint_id="camera_roi",
        event=ENTER,
        timestamp_ns=1_000_000_000,
    )
    notices = state.process_checkpoint(
        apple_id="apple_1",
        checkpoint_id="camera_roi",
        event=EXIT,
        timestamp_ns=2_000_000_000,
    )

    assert "DEADLINE_STARTED" in notice_codes(notices)
    assert state.expire(2_499_999_999) == []
    assert notice_codes(state.expire(2_500_000_000)) == ["TIMEOUT"]
    assert state.expire(3_000_000_000) == []


def test_result_before_deadline_clears_pending_deadline():
    state = MonitorState(500_000_000, "camera_roi")
    state.process_checkpoint(
        apple_id="apple_1",
        checkpoint_id="camera_roi",
        event=EXIT,
        timestamp_ns=2_000_000_000,
    )

    notices = state.process_result(
        inspection_id="inspection_1",
        apple_id="apple_1",
        received_at_ns=2_400_000_000,
    )

    assert "LATE_RESULT" not in notice_codes(notices)
    assert state.expire(3_000_000_000) == []


def test_result_after_timeout_is_late():
    state = MonitorState(500_000_000, "camera_roi")
    state.process_checkpoint(
        apple_id="apple_1",
        checkpoint_id="camera_roi",
        event=EXIT,
        timestamp_ns=2_000_000_000,
    )
    state.expire(2_500_000_000)

    notices = state.process_result(
        inspection_id="inspection_1",
        apple_id="apple_1",
        received_at_ns=2_600_000_000,
    )

    assert "LATE_RESULT" in notice_codes(notices)


def test_result_at_deadline_is_late():
    state = MonitorState(500_000_000, "camera_roi")
    state.process_checkpoint(
        apple_id="apple_1",
        checkpoint_id="camera_roi",
        event=EXIT,
        timestamp_ns=2_000_000_000,
    )

    notices = state.process_result(
        inspection_id="inspection_1",
        apple_id="apple_1",
        received_at_ns=2_500_000_000,
    )

    assert "LATE_RESULT" in notice_codes(notices)


def test_inspection_id_cannot_change_apple_id():
    state = MonitorState(500_000_000)
    state.process_result(
        inspection_id="inspection_1",
        apple_id="apple_1",
        received_at_ns=1,
    )

    notices = state.process_result(
        inspection_id="inspection_1",
        apple_id="apple_2",
        received_at_ns=2,
    )

    assert "ID_MISMATCH" in notice_codes(notices)


def test_id_mismatch_does_not_clear_other_apple_deadline():
    state = MonitorState(500_000_000, "camera_roi")
    state.process_result(
        inspection_id="inspection_1",
        apple_id="apple_1",
        received_at_ns=1,
    )
    state.process_checkpoint(
        apple_id="apple_2",
        checkpoint_id="camera_roi",
        event=EXIT,
        timestamp_ns=2_000_000_000,
    )

    notices = state.process_result(
        inspection_id="inspection_1",
        apple_id="apple_2",
        received_at_ns=2_100_000_000,
    )

    assert notice_codes(notices) == ["ID_MISMATCH"]
    assert notice_codes(state.expire(2_500_000_000)) == ["TIMEOUT"]


def test_invalid_checkpoint_event_is_rejected():
    state = MonitorState(500_000_000)

    notices = state.process_checkpoint(
        apple_id="apple_1",
        checkpoint_id="conveyor_2",
        event=99,
        timestamp_ns=1,
    )

    assert notice_codes(notices) == ["INVALID_CHECKPOINT_EVENT"]
