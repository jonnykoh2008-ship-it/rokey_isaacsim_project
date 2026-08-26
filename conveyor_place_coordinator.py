"""GPU PC 1 shared conveyor Place mutex and ROS status publisher."""

from collections import deque
from dataclasses import dataclass
from typing import Callable, Deque, Optional, Tuple

import rclpy
from appleproj_interfaces.msg import PlaceCoordinatorStatus, SimulationState
from appleproj_interfaces.srv import PlaceCommand
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy


PLACE_STATUS_TOPIC = "/conveyor/place_coordinator_status"
PLACE_COMMAND_SERVICE = "/conveyor/place_command"


@dataclass(frozen=True)
class Reservation:
    robot_id: str
    reservation_id: str
    apple_id: str
    place_position_id: str


@dataclass(frozen=True)
class AdmissionResult:
    accepted: bool
    queued: bool
    error_code: str = ""
    message: str = ""


@dataclass(frozen=True)
class StatusSnapshot:
    state: int
    lock_owner_robot_id: str
    reservation_id: str
    apple_id: str
    place_position_id: str
    waiting_robot_ids: Tuple[str, ...]
    reset_id: int
    scene_version: int
    lock_duration_sec: float
    landing_confirmed: bool
    error_code: str
    message: str


class PlaceCoordinator:
    """FIFO mutex for the one shared Place region.

    Isaac integration calls the transition methods from its simulation thread.
    Every accepted transition and queue change publishes a fresh snapshot.
    """

    def __init__(self, publish_status: Callable[[StatusSnapshot], None]):
        self.publish_status = publish_status
        self.state = PlaceCoordinatorStatus.IDLE
        self.reset_id = 0
        self.scene_version = 0
        self.now_s = 0.0
        self.lock_started_s: Optional[float] = None
        self.active: Optional[Reservation] = None
        self.waiting: Deque[Reservation] = deque()
        self.reservation_ids = set()
        self.landing_confirmed = False
        self.error_code = ""
        self.message = ""

    @staticmethod
    def _clean(value: str) -> str:
        return str(value).strip()

    def _set_time(self, now_s: float) -> None:
        self.now_s = float(now_s)

    def _lock_duration(self) -> float:
        if self.active is None or self.lock_started_s is None:
            return 0.0
        return max(0.0, self.now_s - self.lock_started_s)

    def _snapshot(self) -> StatusSnapshot:
        active = self.active
        return StatusSnapshot(
            state=int(self.state),
            lock_owner_robot_id="" if active is None else active.robot_id,
            reservation_id="" if active is None else active.reservation_id,
            apple_id="" if active is None else active.apple_id,
            place_position_id="" if active is None else active.place_position_id,
            waiting_robot_ids=tuple(item.robot_id for item in self.waiting),
            reset_id=int(self.reset_id),
            scene_version=int(self.scene_version),
            lock_duration_sec=self._lock_duration(),
            landing_confirmed=bool(self.landing_confirmed),
            error_code=str(self.error_code),
            message=str(self.message),
        )

    def _publish(self) -> None:
        self.publish_status(self._snapshot())

    def _reject(self, code: str, message: str) -> AdmissionResult:
        return AdmissionResult(False, False, str(code), str(message))

    def reserve(
        self,
        robot_id: str,
        reservation_id: str,
        apple_id: str,
        place_position_id: str,
        now_s: float,
    ) -> AdmissionResult:
        self._set_time(now_s)
        reservation = Reservation(
            self._clean(robot_id),
            self._clean(reservation_id),
            self._clean(apple_id),
            self._clean(place_position_id),
        )
        if not all(
            (
                reservation.robot_id,
                reservation.reservation_id,
                reservation.apple_id,
                reservation.place_position_id,
            )
        ):
            return self._reject("INVALID_RESERVATION", "required reservation field is empty")
        if reservation.reservation_id in self.reservation_ids:
            return self._reject(
                "DUPLICATE_RESERVATION",
                "reservation_id was already submitted in the current reset generation",
            )

        self.reservation_ids.add(reservation.reservation_id)
        if self.active is None and self.state == PlaceCoordinatorStatus.IDLE:
            self._activate(reservation)
            return AdmissionResult(True, False, message="Place lock reserved")

        self.waiting.append(reservation)
        self.message = "Place reservation queued"
        self._publish()
        return AdmissionResult(True, True, message="Place reservation queued")

    def _activate(self, reservation: Reservation) -> None:
        self.active = reservation
        self.lock_started_s = self.now_s
        self.state = PlaceCoordinatorStatus.RESERVED
        self.landing_confirmed = False
        self.error_code = ""
        self.message = "Place lock reserved"
        self._publish()

    def _matches_owner(self, robot_id: str, reservation_id: str) -> bool:
        return self.active is not None and (
            self.active.robot_id == self._clean(robot_id)
            and self.active.reservation_id == self._clean(reservation_id)
        )

    def start_placing(self, robot_id: str, reservation_id: str, now_s: float) -> AdmissionResult:
        self._set_time(now_s)
        if self.state != PlaceCoordinatorStatus.RESERVED:
            return self._reject("INVALID_STATE", "Place is not in RESERVED state")
        if not self._matches_owner(robot_id, reservation_id):
            return self._reject("LOCK_OWNER_MISMATCH", "robot does not own the Place lock")
        self.state = PlaceCoordinatorStatus.PLACING
        self.message = "PLACE or RELEASE is executing"
        self._publish()
        return AdmissionResult(True, False, message=self.message)

    def release(self, robot_id: str, reservation_id: str, now_s: float) -> AdmissionResult:
        self._set_time(now_s)
        if self.state != PlaceCoordinatorStatus.PLACING:
            return self._reject("INVALID_STATE", "Place is not in PLACING state")
        if not self._matches_owner(robot_id, reservation_id):
            return self._reject("LOCK_OWNER_MISMATCH", "robot does not own the Place lock")
        self.state = PlaceCoordinatorStatus.LANDING_CHECK
        self.message = "RELEASE completed; waiting for conveyor landing confirmation"
        self._publish()
        return AdmissionResult(True, False, message=self.message)

    def confirm_landing(
        self, robot_id: str, reservation_id: str, now_s: float
    ) -> AdmissionResult:
        self._set_time(now_s)
        if self.state != PlaceCoordinatorStatus.LANDING_CHECK:
            return self._reject("INVALID_STATE", "Place is not in LANDING_CHECK state")
        if not self._matches_owner(robot_id, reservation_id):
            return self._reject("LOCK_OWNER_MISMATCH", "robot does not own the Place lock")
        self.state = PlaceCoordinatorStatus.COMPLETED
        self.landing_confirmed = True
        self.message = "apple landing confirmed"
        self._publish()
        self._release_lock("Place cycle completed")
        return AdmissionResult(True, False, message="Place cycle completed")

    def fail(
        self,
        robot_id: str,
        reservation_id: str,
        error_code: str,
        message: str,
        now_s: float,
    ) -> AdmissionResult:
        self._set_time(now_s)
        if self.state not in (
            PlaceCoordinatorStatus.RESERVED,
            PlaceCoordinatorStatus.PLACING,
            PlaceCoordinatorStatus.LANDING_CHECK,
        ):
            return self._reject("INVALID_STATE", "Place cannot enter ERROR from this state")
        if not self._matches_owner(robot_id, reservation_id):
            return self._reject("LOCK_OWNER_MISMATCH", "robot does not own the Place lock")
        if not self._clean(error_code):
            return self._reject("INVALID_ERROR", "error_code is required")
        self.state = PlaceCoordinatorStatus.ERROR
        self.error_code = self._clean(error_code)
        self.message = self._clean(message) or "Place operation failed"
        self._publish()
        return AdmissionResult(True, False, message=self.message)

    def clear_error(
        self,
        robot_id: str,
        reservation_id: str,
        safety_confirmed: bool,
        now_s: float,
    ) -> AdmissionResult:
        self._set_time(now_s)
        if self.state != PlaceCoordinatorStatus.ERROR:
            return self._reject("INVALID_STATE", "Place is not in ERROR state")
        if not self._matches_owner(robot_id, reservation_id):
            return self._reject("LOCK_OWNER_MISMATCH", "robot does not own the Place lock")
        if not safety_confirmed:
            return self._reject("SAFETY_NOT_CONFIRMED", "safe lock release is not confirmed")
        self._release_lock("ERROR cleared after safety confirmation")
        return AdmissionResult(True, False, message="Place error cleared")

    def _release_lock(self, message: str) -> None:
        self.active = None
        self.lock_started_s = None
        self.state = PlaceCoordinatorStatus.IDLE
        self.landing_confirmed = False
        self.error_code = ""
        self.message = str(message)
        self._publish()
        if self.waiting:
            self._activate(self.waiting.popleft())

    def reset(self, reset_id: int, scene_version: int, now_s: float) -> None:
        self._set_time(now_s)
        self.reset_id = int(reset_id)
        self.scene_version = int(scene_version)
        self.active = None
        self.waiting.clear()
        self.reservation_ids.clear()
        self.lock_started_s = None
        self.state = PlaceCoordinatorStatus.IDLE
        self.landing_confirmed = False
        self.error_code = ""
        self.message = "Place reservations cleared for simulation generation"
        self._publish()


class PlaceCoordinatorNode(Node):
    """ROS adapter for status publication and Isaac simulation-generation reset."""

    def __init__(self):
        super().__init__(
            "conveyor_place_coordinator",
            parameter_overrides=[Parameter("use_sim_time", value=True)],
        )
        latched_qos = QoSProfile(
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
        )
        self.status_publisher = self.create_publisher(
            PlaceCoordinatorStatus, PLACE_STATUS_TOPIC, latched_qos
        )
        self.controller = PlaceCoordinator(self._publish_status)
        self._generation: Optional[Tuple[int, int]] = None
        self.create_subscription(
            SimulationState, "/simulation/state", self._on_simulation_state, latched_qos
        )
        self.command_service = self.create_service(
            PlaceCommand, PLACE_COMMAND_SERVICE, self._on_command
        )
        self.controller.reset(0, 0, self._now_s())

    def _now_s(self) -> float:
        return self.get_clock().now().nanoseconds / 1_000_000_000.0

    def _publish_status(self, snapshot: StatusSnapshot) -> None:
        value = PlaceCoordinatorStatus()
        value.header.stamp = self.get_clock().now().to_msg()
        value.header.frame_id = "world"
        value.state = snapshot.state
        value.lock_owner_robot_id = snapshot.lock_owner_robot_id
        value.reservation_id = snapshot.reservation_id
        value.apple_id = snapshot.apple_id
        value.place_position_id = snapshot.place_position_id
        value.waiting_robot_ids = list(snapshot.waiting_robot_ids)
        value.reset_id = snapshot.reset_id
        value.scene_version = snapshot.scene_version
        value.lock_duration_sec = snapshot.lock_duration_sec
        value.landing_confirmed = snapshot.landing_confirmed
        value.error_code = snapshot.error_code
        value.message = snapshot.message
        self.status_publisher.publish(value)

    def _on_simulation_state(self, message: SimulationState) -> None:
        generation = (int(message.reset_id), int(message.scene_version))
        if generation != self._generation:
            self._generation = generation
            self.controller.reset(*generation, self._now_s())

    def _on_command(self, request: PlaceCommand.Request, response: PlaceCommand.Response):
        generation = (int(request.reset_id), int(request.scene_version))
        current = (self.controller.reset_id, self.controller.scene_version)
        if generation != current:
            result = AdmissionResult(
                False,
                False,
                "GENERATION_MISMATCH",
                f"request generation {generation} does not match current {current}",
            )
        else:
            now_s = self._now_s()
            if request.command == PlaceCommand.Request.RESERVE:
                result = self.controller.reserve(
                    request.robot_id,
                    request.reservation_id,
                    request.apple_id,
                    request.place_position_id,
                    now_s,
                )
            elif request.command == PlaceCommand.Request.START_PLACING:
                result = self.controller.start_placing(
                    request.robot_id, request.reservation_id, now_s
                )
            elif request.command == PlaceCommand.Request.RELEASED:
                result = self.controller.release(
                    request.robot_id, request.reservation_id, now_s
                )
            elif request.command == PlaceCommand.Request.CONFIRM_LANDING:
                result = self.controller.confirm_landing(
                    request.robot_id, request.reservation_id, now_s
                )
            elif request.command == PlaceCommand.Request.FAIL:
                result = self.controller.fail(
                    request.robot_id,
                    request.reservation_id,
                    request.error_code,
                    request.message,
                    now_s,
                )
            elif request.command == PlaceCommand.Request.CLEAR_ERROR:
                result = self.controller.clear_error(
                    request.robot_id,
                    request.reservation_id,
                    request.safety_confirmed,
                    now_s,
                )
            else:
                result = AdmissionResult(
                    False, False, "INVALID_COMMAND", "unknown Place command"
                )
        response.accepted = bool(result.accepted)
        response.queued = bool(result.queued)
        response.state = int(self.controller.state)
        response.error_code = result.error_code
        response.message = result.message
        return response


def main():
    rclpy.init()
    node = PlaceCoordinatorNode()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
