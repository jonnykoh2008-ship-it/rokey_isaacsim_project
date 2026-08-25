"""ROS-independent state tracking for quality and checkpoint monitoring."""

from dataclasses import dataclass


ENTER = 1
EXIT = 2


@dataclass(frozen=True)
class MonitorNotice:
    """A state transition that should be reported by the ROS node."""

    level: str
    code: str
    message: str


@dataclass(frozen=True)
class Deadline:
    inspection_id: str
    apple_id: str
    expires_at_ns: int


class MonitorState:
    """Correlate quality results and checkpoint events by stable identifiers."""

    def __init__(self, deadline_ns: int, deadline_checkpoint_id: str = "") -> None:
        if deadline_ns <= 0:
            raise ValueError("deadline_ns must be positive")
        self.deadline_ns = deadline_ns
        self.deadline_checkpoint_id = deadline_checkpoint_id
        self._entered: set[tuple[str, str]] = set()
        self._seen_checkpoint_apples: set[str] = set()
        self._inspection_to_apple: dict[str, str] = {}
        self._latest_inspection_by_apple: dict[str, str] = {}
        self._pending: dict[str, Deadline] = {}
        self._timed_out: dict[str, Deadline] = {}

    @property
    def deadline_enabled(self) -> bool:
        return bool(self.deadline_checkpoint_id)

    def process_checkpoint(
        self,
        *,
        apple_id: str,
        checkpoint_id: str,
        event: int,
        timestamp_ns: int,
    ) -> list[MonitorNotice]:
        notices: list[MonitorNotice] = []
        if not apple_id or not checkpoint_id:
            return [
                MonitorNotice(
                    "error",
                    "INVALID_CHECKPOINT",
                    "CheckpointEvent has an empty apple_id or checkpoint_id",
                )
            ]
        if event not in (ENTER, EXIT):
            return [
                MonitorNotice(
                    "error",
                    "INVALID_CHECKPOINT_EVENT",
                    f"Unknown checkpoint event value {event}",
                )
            ]

        self._seen_checkpoint_apples.add(apple_id)
        checkpoint_key = (apple_id, checkpoint_id)
        if event == ENTER:
            if checkpoint_key in self._entered:
                notices.append(
                    MonitorNotice(
                        "warning",
                        "DUPLICATE_ENTER",
                        f"Duplicate ENTER for apple={apple_id} checkpoint={checkpoint_id}",
                    )
                )
            self._entered.add(checkpoint_key)
            return notices

        if checkpoint_key not in self._entered:
            notices.append(
                MonitorNotice(
                    "warning",
                    "EXIT_WITHOUT_ENTER",
                    f"EXIT without ENTER for apple={apple_id} checkpoint={checkpoint_id}",
                )
            )
        else:
            self._entered.remove(checkpoint_key)

        if checkpoint_id != self.deadline_checkpoint_id:
            return notices

        inspection_id = self._latest_inspection_by_apple.get(apple_id, "")
        deadline = Deadline(
            inspection_id=inspection_id,
            apple_id=apple_id,
            expires_at_ns=timestamp_ns + self.deadline_ns,
        )
        self._pending[apple_id] = deadline
        self._timed_out.pop(apple_id, None)
        notices.append(
            MonitorNotice(
                "info",
                "DEADLINE_STARTED",
                f"Result deadline started for apple={apple_id}",
            )
        )
        return notices

    def process_result(
        self,
        *,
        inspection_id: str,
        apple_id: str,
        received_at_ns: int,
    ) -> list[MonitorNotice]:
        if not inspection_id or not apple_id:
            return [
                MonitorNotice(
                    "error",
                    "INVALID_RESULT",
                    "QualityResult has an empty inspection_id or apple_id",
                )
            ]

        notices: list[MonitorNotice] = []
        known_apple = self._inspection_to_apple.get(inspection_id)
        if known_apple is not None and known_apple != apple_id:
            return [
                MonitorNotice(
                    "error",
                    "ID_MISMATCH",
                    (
                        f"inspection={inspection_id} changed apple_id "
                        f"from {known_apple} to {apple_id}"
                    ),
                )
            ]

        self._inspection_to_apple[inspection_id] = apple_id

        self._latest_inspection_by_apple[apple_id] = inspection_id
        if apple_id not in self._seen_checkpoint_apples:
            notices.append(
                MonitorNotice(
                    "warning",
                    "RESULT_WITHOUT_CHECKPOINT",
                    f"Result received before any checkpoint for apple={apple_id}",
                )
            )

        timed_out = self._timed_out.pop(apple_id, None)
        pending = self._pending.pop(apple_id, None)
        deadline = timed_out or pending
        if deadline is not None and received_at_ns >= deadline.expires_at_ns:
            notices.append(
                MonitorNotice(
                    "warning",
                    "LATE_RESULT",
                    f"Result arrived after deadline for apple={apple_id}",
                )
            )
        return notices

    def expire(self, now_ns: int) -> list[MonitorNotice]:
        notices: list[MonitorNotice] = []
        expired_apple_ids = [
            apple_id
            for apple_id, deadline in self._pending.items()
            if now_ns >= deadline.expires_at_ns
        ]
        for apple_id in expired_apple_ids:
            deadline = self._pending.pop(apple_id)
            self._timed_out[apple_id] = deadline
            notices.append(
                MonitorNotice(
                    "error",
                    "TIMEOUT",
                    f"No quality result before deadline for apple={apple_id}",
                )
            )
        return notices
