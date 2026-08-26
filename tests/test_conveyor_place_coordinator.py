import unittest

from appleproj_interfaces.msg import PlaceCoordinatorStatus
from appleproj_interfaces.srv import PlaceCommand

from conveyor_place_coordinator import PlaceCoordinator


class PlaceCoordinatorTest(unittest.TestCase):
    def test_place_command_contract_contains_all_lifecycle_commands(self):
        self.assertEqual(
            [1, 2, 3, 4, 5, 6],
            [
                PlaceCommand.Request.RESERVE,
                PlaceCommand.Request.START_PLACING,
                PlaceCommand.Request.RELEASED,
                PlaceCommand.Request.CONFIRM_LANDING,
                PlaceCommand.Request.FAIL,
                PlaceCommand.Request.CLEAR_ERROR,
            ],
        )

    def setUp(self):
        self.statuses = []
        self.controller = PlaceCoordinator(self.statuses.append)
        self.controller.reset(4, 7, 10.0)
        self.statuses.clear()

    def reserve(self, robot="robot_01", reservation="reservation-1", apple="apple-1"):
        return self.controller.reserve(robot, reservation, apple, "shared_place", 11.0)

    def test_first_reservation_owns_lock_and_required_fields(self):
        result = self.reserve()

        self.assertTrue(result.accepted)
        self.assertFalse(result.queued)
        status = self.statuses[-1]
        self.assertEqual(PlaceCoordinatorStatus.RESERVED, status.state)
        self.assertEqual("robot_01", status.lock_owner_robot_id)
        self.assertEqual("reservation-1", status.reservation_id)
        self.assertEqual("apple-1", status.apple_id)
        self.assertEqual("shared_place", status.place_position_id)
        self.assertEqual((4, 7), (status.reset_id, status.scene_version))

    def test_waiting_reservations_are_fifo(self):
        self.reserve()
        queued = self.controller.reserve(
            "robot_02", "reservation-2", "apple-2", "shared_place", 11.1
        )
        self.controller.reserve(
            "robot_01", "reservation-3", "apple-3", "shared_place", 11.2
        )

        self.assertTrue(queued.queued)
        self.assertEqual(("robot_02", "robot_01"), self.statuses[-1].waiting_robot_ids)
        self.controller.start_placing("robot_01", "reservation-1", 12.0)
        self.controller.release("robot_01", "reservation-1", 13.0)
        self.controller.confirm_landing("robot_01", "reservation-1", 14.0)

        self.assertEqual(
            [PlaceCoordinatorStatus.COMPLETED, PlaceCoordinatorStatus.IDLE, PlaceCoordinatorStatus.RESERVED],
            [item.state for item in self.statuses[-3:]],
        )
        self.assertEqual("robot_02", self.statuses[-1].lock_owner_robot_id)

    def test_duplicate_reservation_id_is_rejected(self):
        self.reserve()
        duplicate = self.controller.reserve(
            "robot_02", "reservation-1", "apple-2", "shared_place", 11.5
        )

        self.assertFalse(duplicate.accepted)
        self.assertEqual("DUPLICATE_RESERVATION", duplicate.error_code)
        self.assertEqual(1, len(self.statuses))

    def test_non_owner_cannot_enter_place(self):
        self.reserve()
        result = self.controller.start_placing("robot_02", "reservation-1", 12.0)

        self.assertFalse(result.accepted)
        self.assertEqual("LOCK_OWNER_MISMATCH", result.error_code)
        self.assertEqual(PlaceCoordinatorStatus.RESERVED, self.statuses[-1].state)

    def test_lock_is_held_until_landing_confirmation(self):
        self.reserve()
        self.controller.start_placing("robot_01", "reservation-1", 12.0)
        self.controller.release("robot_01", "reservation-1", 13.0)

        status = self.statuses[-1]
        self.assertEqual(PlaceCoordinatorStatus.LANDING_CHECK, status.state)
        self.assertEqual("robot_01", status.lock_owner_robot_id)
        self.assertFalse(status.landing_confirmed)

        self.controller.confirm_landing("robot_01", "reservation-1", 15.0)
        completed, idle = self.statuses[-2:]
        self.assertTrue(completed.landing_confirmed)
        self.assertEqual("robot_01", completed.lock_owner_robot_id)
        self.assertEqual("", idle.lock_owner_robot_id)
        self.assertEqual(0.0, idle.lock_duration_sec)

    def test_error_retains_lock_until_explicit_safety_confirmation(self):
        self.reserve()
        self.controller.start_placing("robot_01", "reservation-1", 12.0)
        self.controller.fail(
            "robot_01", "reservation-1", "LANDING_SENSOR_FAILURE", "sensor unavailable", 13.0
        )

        denied = self.controller.clear_error(
            "robot_01", "reservation-1", False, 14.0
        )
        self.assertEqual("SAFETY_NOT_CONFIRMED", denied.error_code)
        self.assertEqual(PlaceCoordinatorStatus.ERROR, self.statuses[-1].state)
        self.assertEqual("robot_01", self.statuses[-1].lock_owner_robot_id)

        cleared = self.controller.clear_error(
            "robot_01", "reservation-1", True, 15.0
        )
        self.assertTrue(cleared.accepted)
        self.assertEqual(PlaceCoordinatorStatus.IDLE, self.statuses[-1].state)

    def test_reset_discards_lock_queue_and_duplicate_cache(self):
        self.reserve()
        self.controller.reserve(
            "robot_02", "reservation-2", "apple-2", "shared_place", 11.1
        )

        self.controller.reset(5, 8, 1.0)
        status = self.statuses[-1]
        self.assertEqual(PlaceCoordinatorStatus.IDLE, status.state)
        self.assertEqual((), status.waiting_robot_ids)
        self.assertEqual((5, 8), (status.reset_id, status.scene_version))
        self.assertEqual("", status.reservation_id)
        self.assertTrue(self.reserve().accepted)

    def test_lock_duration_uses_supplied_simulation_time(self):
        self.reserve()
        self.controller.start_placing("robot_01", "reservation-1", 13.5)
        first_duration = self.statuses[-1].lock_duration_sec
        self.controller.release("robot_01", "reservation-1", 13.5)

        self.assertEqual(2.5, first_duration)
        self.assertEqual(first_duration, self.statuses[-1].lock_duration_sec)


if __name__ == "__main__":
    unittest.main()
