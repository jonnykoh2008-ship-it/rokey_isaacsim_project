"""GPU PC 1 conveyor pusher command validation and execution state machine.

ROS callbacks only enqueue work.  ``SortRuntime.process`` must be called from the
Isaac Sim main thread because its controller touches articulation handles.
"""

from __future__ import annotations

import queue
import threading
from dataclasses import dataclass, field
from typing import Callable, Dict, Optional, Protocol, Tuple

from appleproj_interfaces.msg import CheckpointEvent, SortStatus
from appleproj_interfaces.srv import SortCommand
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy


GRADE_TO_PUSHER = {
    SortCommand.Request.HIGH: SortCommand.Request.PUSHER_1,
    SortCommand.Request.MEDIUM: SortCommand.Request.PUSHER_2,
    SortCommand.Request.LOW: SortCommand.Request.PUSHER_3,
}
PUSHER_TO_TRIGGER = {
    SortCommand.Request.PUSHER_1: "CONVEYOR_PUSHER_1_TRIGGER",
    SortCommand.Request.PUSHER_2: "CONVEYOR_PUSHER_2_TRIGGER",
    SortCommand.Request.PUSHER_3: "CONVEYOR_PUSHER_3_TRIGGER",
}
VALID_ERROR_CODES = {
    "INVALID_COMMAND",
    "INVALID_GRADE",
    "INVALID_PUSHER",
    "GRADE_PUSHER_MISMATCH",
    "INVALID_TRIGGER",
    "DUPLICATE_COMMAND_CONFLICT",
    "APPLE_ALREADY_SORTED",
    "PUSHER_BUSY",
    "PUSHER_NOT_HOME",
    "APPLE_ID_MISMATCH",
    "TRIGGER_TIMEOUT",
    "PUSH_TIMEOUT",
    "JAM_DETECTED",
    "HOME_TIMEOUT",
    "SIMULATION_RESET",
    "CANCELLED",
    "INTERNAL_ERROR",
}


class PusherActuator(Protocol):
    """Main-thread-only Isaac pusher adapter."""

    @property
    def available(self) -> bool: ...

    def is_home(self, pusher_id: int) -> bool: ...

    def begin_extend(self, pusher_id: int) -> None: ...

    def is_extended(self, pusher_id: int) -> bool: ...

    def begin_retract(self, pusher_id: int) -> None: ...

    def is_jammed(self, pusher_id: int) -> bool: ...

    def progress(self, pusher_id: int, extending: bool) -> float: ...

    def stop_all(self) -> None: ...

    def try_home_all(self) -> None: ...


@dataclass(frozen=True)
class TimingConfig:
    trigger_timeout_s: float
    push_timeout_s: float
    home_timeout_s: float

    def __post_init__(self) -> None:
        for name, value in (
            ("trigger_timeout_s", self.trigger_timeout_s),
            ("push_timeout_s", self.push_timeout_s),
            ("home_timeout_s", self.home_timeout_s),
        ):
            if value <= 0.0:
                raise ValueError(f"{name} must be greater than zero")


@dataclass(frozen=True)
class CommandData:
    command_id: str
    apple_id: str
    inspection_id: str
    grade: int
    pusher_id: int
    trigger_checkpoint_id: str

    @classmethod
    def from_request(cls, request: SortCommand.Request) -> "CommandData":
        return cls(
            command_id=str(request.command_id),
            apple_id=str(request.apple_id),
            inspection_id=str(request.inspection_id),
            grade=int(request.grade),
            pusher_id=int(request.pusher_id),
            trigger_checkpoint_id=str(request.trigger_checkpoint_id),
        )


@dataclass(frozen=True)
class AdmissionResult:
    accepted: bool
    command_id: str
    error_code: str
    message: str


@dataclass
class CommandRecord:
    data: CommandData
    state: int = SortStatus.ARMED
    state_started_s: float = 0.0
    response: AdmissionResult = field(init=False)

    def __post_init__(self) -> None:
        self.response = AdmissionResult(True, self.data.command_id, "", "command armed")


class SortController:
    """Deterministic single-pusher-at-a-time state machine."""

    def __init__(
        self,
        actuator: PusherActuator,
        timing: TimingConfig,
        publish_status: Callable[[CommandData, int, float, str, str], None],
    ) -> None:
        self.actuator = actuator
        self.timing = timing
        self.publish_status = publish_status
        self.simulation_ready = False
        self.now_s = 0.0
        self.active: Optional[CommandRecord] = None
        self.command_cache: Dict[str, Tuple[CommandData, AdmissionResult]] = {}
        self.sorted_apples = set()
        self.occupied_triggers = set()
        self.consumed_trigger_dwells = set()

    @staticmethod
    def _reject(command_id: str, code: str, message: str) -> AdmissionResult:
        if code not in VALID_ERROR_CODES:
            raise ValueError(f"unknown sort error code: {code}")
        return AdmissionResult(False, command_id, code, message)

    def submit(self, request: SortCommand.Request, now_s: float) -> AdmissionResult:
        data = CommandData.from_request(request)
        self.now_s = float(now_s)
        cached = self.command_cache.get(data.command_id)
        if cached is not None:
            cached_data, cached_response = cached
            if data == cached_data:
                return cached_response
            return self._reject(
                data.command_id,
                "DUPLICATE_COMMAND_CONFLICT",
                "command_id is already associated with different content",
            )

        result = self._validate_new(data)
        if not result.accepted:
            return result
        record = CommandRecord(data=data, state_started_s=self.now_s)
        self.active = record
        self.command_cache[data.command_id] = (data, record.response)
        self._publish(record, SortStatus.ARMED, 0.0, "", "command armed")
        return record.response

    def _validate_new(self, data: CommandData) -> AdmissionResult:
        if not data.command_id or not data.apple_id or not data.inspection_id:
            return self._reject(data.command_id, "INVALID_COMMAND", "required identifier is empty")
        if data.grade not in GRADE_TO_PUSHER:
            return self._reject(data.command_id, "INVALID_GRADE", "grade is not valid")
        if data.pusher_id not in PUSHER_TO_TRIGGER:
            return self._reject(data.command_id, "INVALID_PUSHER", "pusher_id is not valid")
        if GRADE_TO_PUSHER[data.grade] != data.pusher_id:
            return self._reject(
                data.command_id, "GRADE_PUSHER_MISMATCH", "grade and pusher mapping do not match"
            )
        if PUSHER_TO_TRIGGER[data.pusher_id] != data.trigger_checkpoint_id:
            return self._reject(
                data.command_id, "INVALID_TRIGGER", "trigger does not match selected pusher"
            )
        if data.apple_id in self.sorted_apples:
            return self._reject(
                data.command_id, "APPLE_ALREADY_SORTED", "apple was already sorted"
            )
        if not self.simulation_ready:
            return self._reject(
                data.command_id, "INVALID_COMMAND", "simulation is resetting or stopped"
            )
        if self.active is not None:
            return self._reject(data.command_id, "PUSHER_BUSY", "another sort command is active")
        if not self.actuator.available or not self.actuator.is_home(data.pusher_id):
            return self._reject(
                data.command_id, "PUSHER_NOT_HOME", "selected pusher home is not confirmed"
            )
        if any(
            not self.actuator.is_home(pusher_id) for pusher_id in PUSHER_TO_TRIGGER
        ):
            return self._reject(
                data.command_id, "PUSHER_BUSY", "another pusher is away from home"
            )
        return AdmissionResult(True, data.command_id, "", "command armed")

    def checkpoint(self, checkpoint_id: str, apple_id: str, entered: bool, now_s: float) -> None:
        self.now_s = float(now_s)
        dwell = (str(checkpoint_id), str(apple_id))
        if not entered:
            self.occupied_triggers.discard(dwell)
            self.consumed_trigger_dwells.discard(dwell)
            return
        if dwell in self.occupied_triggers:
            return
        self.occupied_triggers.add(dwell)
        record = self.active
        if record is None or record.state != SortStatus.ARMED:
            return
        if checkpoint_id != record.data.trigger_checkpoint_id:
            return
        if apple_id != record.data.apple_id:
            self._fail(record, "APPLE_ID_MISMATCH", "trigger apple_id does not match command")
            return
        if dwell in self.consumed_trigger_dwells:
            return
        if not self.actuator.is_home(record.data.pusher_id):
            self._fail(record, "PUSHER_NOT_HOME", "pusher left home before trigger confirmation")
            return
        if any(
            pusher_id != record.data.pusher_id and not self.actuator.is_home(pusher_id)
            for pusher_id in PUSHER_TO_TRIGGER
        ):
            self._fail(record, "PUSHER_BUSY", "another pusher is away from home")
            return
        self.consumed_trigger_dwells.add(dwell)
        self._publish(record, SortStatus.APPLE_CONFIRMED, 0.2, "", "apple confirmed at trigger")
        try:
            self.actuator.begin_extend(record.data.pusher_id)
        except Exception as exc:  # Isaac errors must become an observable terminal state.
            self._fail(record, "INTERNAL_ERROR", f"failed to start extension: {exc}")
            return
        self._publish(record, SortStatus.EXTENDING, 0.25, "", "pusher extending")

    def tick(self, now_s: float) -> None:
        self.now_s = float(now_s)
        record = self.active
        if record is None:
            return
        elapsed = self.now_s - record.state_started_s
        pusher_id = record.data.pusher_id
        try:
            if record.state == SortStatus.ARMED:
                if elapsed >= self.timing.trigger_timeout_s:
                    self._fail(record, "TRIGGER_TIMEOUT", "apple did not reach trigger in time")
            elif record.state == SortStatus.EXTENDING:
                if self.actuator.is_jammed(pusher_id):
                    self._fail(record, "JAM_DETECTED", "pusher jam threshold exceeded")
                elif self.actuator.is_extended(pusher_id):
                    self._publish(
                        record, SortStatus.PUSH_CONFIRMED, 0.6, "", "extension confirmed"
                    )
                    self.actuator.begin_retract(pusher_id)
                    self._publish(record, SortStatus.RETRACTING, 0.65, "", "pusher retracting")
                elif elapsed >= self.timing.push_timeout_s:
                    self._fail(record, "PUSH_TIMEOUT", "pusher extension timed out")
                else:
                    self._publish(
                        record,
                        SortStatus.EXTENDING,
                        0.25 + 0.35 * self.actuator.progress(pusher_id, True),
                        "",
                        "pusher extending",
                    )
            elif record.state == SortStatus.RETRACTING:
                if self.actuator.is_jammed(pusher_id):
                    self._fail(record, "JAM_DETECTED", "pusher jam threshold exceeded")
                elif self.actuator.is_home(pusher_id):
                    self._publish(
                        record, SortStatus.HOME_CONFIRMED, 0.95, "", "home confirmed"
                    )
                    self.sorted_apples.add(record.data.apple_id)
                    self._publish(record, SortStatus.COMPLETED, 1.0, "", "sorting completed")
                    self.active = None
                elif elapsed >= self.timing.home_timeout_s:
                    self._fail(record, "HOME_TIMEOUT", "pusher did not return home in time")
                else:
                    self._publish(
                        record,
                        SortStatus.RETRACTING,
                        0.65 + 0.3 * self.actuator.progress(pusher_id, False),
                        "",
                        "pusher retracting",
                    )
        except Exception as exc:
            self._fail(record, "INTERNAL_ERROR", f"pusher state read failed: {exc}")

    def cancel(self, error_code: str = "CANCELLED", message: str = "sorting cancelled") -> None:
        record = self.active
        if record is None:
            return
        self._safe_stop_and_home()
        self._publish(record, SortStatus.CANCELLED, 0.0, error_code, message)
        self.active = None

    def reset(self) -> None:
        if self.active is not None:
            self.cancel("SIMULATION_RESET", "simulation stopped or reset")
        else:
            self._safe_stop_and_home()
        self.command_cache.clear()
        self.sorted_apples.clear()
        self.occupied_triggers.clear()
        self.consumed_trigger_dwells.clear()
        self.simulation_ready = False

    def _fail(self, record: CommandRecord, code: str, message: str) -> None:
        self._safe_stop_and_home()
        self._publish(record, SortStatus.FAILED, 0.0, code, message)
        self.active = None

    def _safe_stop_and_home(self) -> None:
        try:
            self.actuator.stop_all()
        except Exception:
            pass
        try:
            self.actuator.try_home_all()
        except Exception:
            pass

    def _publish(
        self, record: CommandRecord, state: int, progress: float, error_code: str, message: str
    ) -> None:
        changed = record.state != int(state)
        record.state = int(state)
        if changed:
            record.state_started_s = self.now_s
        self.publish_status(record.data, int(state), float(progress), error_code, message)


@dataclass
class _PendingService:
    request: SortCommand.Request
    done: threading.Event = field(default_factory=threading.Event)
    result: Optional[AdmissionResult] = None


class SortRuntime:
    """ROS transport adapter whose ``process`` method belongs to the Isaac thread."""

    def __init__(self, node, actuator: PusherActuator, timing: TimingConfig) -> None:
        self.node = node
        self.events = queue.Queue()
        qos = QoSProfile(
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
        )
        checkpoint_qos = QoSProfile(
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
        )
        self.publisher = node.create_publisher(SortStatus, "/conveyor/sort_status", qos)
        self.service = node.create_service(
            SortCommand, "/conveyor/sort_command", self._on_service
        )
        self.subscription = node.create_subscription(
            CheckpointEvent,
            "/conveyor/checkpoint_events",
            self._on_checkpoint,
            checkpoint_qos,
        )
        self.controller = SortController(actuator, timing, self._publish_status)

    def _on_service(self, request, response):
        pending = _PendingService(request=request)
        self.events.put(("service", pending))
        pending.done.wait()
        result = pending.result
        response.accepted = bool(result.accepted)
        response.command_id = result.command_id
        response.error_code = result.error_code
        response.message = result.message
        return response

    def _on_checkpoint(self, message: CheckpointEvent) -> None:
        self.events.put(
            (
                "checkpoint",
                (
                    message.checkpoint_id,
                    message.apple_id,
                    message.event == CheckpointEvent.ENTER,
                ),
            )
        )

    def process(self, simulation_time_s: float, simulation_ready: bool = True) -> None:
        self.controller.simulation_ready = bool(simulation_ready)
        while True:
            try:
                kind, payload = self.events.get_nowait()
            except queue.Empty:
                break
            if kind == "service":
                pending = payload
                pending.result = self.controller.submit(pending.request, simulation_time_s)
                pending.done.set()
            else:
                checkpoint_id, apple_id, entered = payload
                self.controller.checkpoint(
                    checkpoint_id, apple_id, entered, simulation_time_s
                )
        self.controller.tick(simulation_time_s)

    def reset(self) -> None:
        self.controller.reset()
        while True:
            try:
                kind, payload = self.events.get_nowait()
            except queue.Empty:
                break
            if kind == "service":
                pending = payload
                pending.result = AdmissionResult(
                    False,
                    str(pending.request.command_id),
                    "INVALID_COMMAND",
                    "simulation reset",
                )
                pending.done.set()

    def _publish_status(
        self, data: CommandData, state: int, progress: float, error_code: str, message: str
    ) -> None:
        value = SortStatus()
        value.header.stamp = self.node.get_clock().now().to_msg()
        value.header.frame_id = "world"
        value.command_id = data.command_id
        value.apple_id = data.apple_id
        value.inspection_id = data.inspection_id
        value.grade = data.grade
        value.pusher_id = data.pusher_id
        value.trigger_checkpoint_id = data.trigger_checkpoint_id
        value.state = int(state)
        value.progress = max(0.0, min(1.0, float(progress)))
        value.error_code = error_code
        value.message = message
        self.publisher.publish(value)
