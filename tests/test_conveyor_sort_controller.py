import unittest

from appleproj_interfaces.msg import SortStatus
from appleproj_interfaces.srv import SortCommand

from conveyor_sort_controller import SortController, TimingConfig


class FakeActuator:
    available = True

    def __init__(self):
        self.home = {1: True, 2: True, 3: True}
        self.extended = {1: False, 2: False, 3: False}
        self.jammed = False
        self.extend_calls = []
        self.retract_calls = []
        self.stop_calls = 0
        self.home_calls = 0

    def is_home(self, pusher_id):
        return self.home[pusher_id]

    def begin_extend(self, pusher_id):
        self.home[pusher_id] = False
        self.extend_calls.append(pusher_id)

    def is_extended(self, pusher_id):
        return self.extended[pusher_id]

    def begin_retract(self, pusher_id):
        self.extended[pusher_id] = False
        self.retract_calls.append(pusher_id)

    def is_jammed(self, _pusher_id):
        return self.jammed

    def progress(self, _pusher_id, _extending):
        return 0.5

    def stop_all(self):
        self.stop_calls += 1

    def try_home_all(self):
        self.home_calls += 1


class ConveyorSortControllerTest(unittest.TestCase):
    def setUp(self):
        self.actuator = FakeActuator()
        self.statuses = []
        self.controller = SortController(
            self.actuator,
            TimingConfig(trigger_timeout_s=5.0, push_timeout_s=2.0, home_timeout_s=3.0),
            lambda data, state, progress, error, message: self.statuses.append(
                (data, state, progress, error, message)
            ),
        )
        self.controller.simulation_ready = True

    @staticmethod
    def request(
        command_id="command-1",
        apple_id="apple-1",
        inspection_id="inspection-1",
        grade=SortCommand.Request.HIGH,
        pusher_id=SortCommand.Request.PUSHER_1,
        trigger="CONVEYOR_PUSHER_1_TRIGGER",
    ):
        value = SortCommand.Request()
        value.command_id = command_id
        value.apple_id = apple_id
        value.inspection_id = inspection_id
        value.grade = grade
        value.pusher_id = pusher_id
        value.trigger_checkpoint_id = trigger
        return value

    def test_accepts_valid_command_and_publishes_armed(self):
        result = self.controller.submit(self.request(), 1.0)

        self.assertTrue(result.accepted)
        self.assertEqual("", result.error_code)
        self.assertEqual(SortStatus.ARMED, self.statuses[-1][1])

    def test_rejects_required_identifier_and_mapping_errors(self):
        cases = [
            (self.request(command_id=""), "INVALID_COMMAND"),
            (self.request(grade=99), "INVALID_GRADE"),
            (self.request(pusher_id=99), "INVALID_PUSHER"),
            (
                self.request(
                    pusher_id=SortCommand.Request.PUSHER_2,
                    trigger="CONVEYOR_PUSHER_2_TRIGGER",
                ),
                "GRADE_PUSHER_MISMATCH",
            ),
            (self.request(trigger="WRONG_TRIGGER"), "INVALID_TRIGGER"),
        ]
        for request, expected in cases:
            with self.subTest(expected=expected):
                result = self.controller.submit(request, 1.0)
                self.assertFalse(result.accepted)
                self.assertEqual(expected, result.error_code)

    def test_rejects_when_simulation_not_ready_or_pusher_not_home(self):
        self.controller.simulation_ready = False
        result = self.controller.submit(self.request(), 1.0)
        self.assertEqual("INVALID_COMMAND", result.error_code)

        self.controller.simulation_ready = True
        self.actuator.home[1] = False
        result = self.controller.submit(self.request(command_id="command-2"), 1.0)
        self.assertEqual("PUSHER_NOT_HOME", result.error_code)

        self.actuator.home[1] = True
        self.actuator.home[2] = False
        result = self.controller.submit(self.request(command_id="command-3"), 1.0)
        self.assertEqual("PUSHER_BUSY", result.error_code)

    def test_duplicate_same_request_is_idempotent_and_conflict_is_rejected(self):
        request = self.request()
        first = self.controller.submit(request, 1.0)
        second = self.controller.submit(request, 1.1)
        conflict = self.controller.submit(self.request(apple_id="apple-2"), 1.2)

        self.assertEqual(first, second)
        self.assertEqual(1, len(self.statuses))
        self.assertEqual("DUPLICATE_COMMAND_CONFLICT", conflict.error_code)

    def test_rejects_second_command_while_busy(self):
        self.controller.submit(self.request(), 1.0)
        result = self.controller.submit(
            self.request(command_id="command-2", apple_id="apple-2"), 1.1
        )
        self.assertEqual("PUSHER_BUSY", result.error_code)

    def test_matching_checkpoint_executes_complete_state_flow(self):
        self.controller.submit(self.request(), 1.0)
        self.controller.checkpoint(
            "CONVEYOR_PUSHER_1_TRIGGER", "apple-1", True, 2.0
        )
        self.assertEqual([1], self.actuator.extend_calls)

        self.actuator.extended[1] = True
        self.controller.tick(2.5)
        self.actuator.home[1] = True
        self.controller.tick(3.0)

        states = [item[1] for item in self.statuses]
        self.assertEqual(
            [
                SortStatus.ARMED,
                SortStatus.APPLE_CONFIRMED,
                SortStatus.EXTENDING,
                SortStatus.PUSH_CONFIRMED,
                SortStatus.RETRACTING,
                SortStatus.HOME_CONFIRMED,
                SortStatus.COMPLETED,
            ],
            states,
        )
        self.assertIsNone(self.controller.active)
        result = self.controller.submit(
            self.request(command_id="command-2"), 3.1
        )
        self.assertEqual("APPLE_ALREADY_SORTED", result.error_code)

    def test_same_trigger_dwell_does_not_extend_twice(self):
        self.controller.submit(self.request(), 1.0)
        for timestamp in (2.0, 2.1):
            self.controller.checkpoint(
                "CONVEYOR_PUSHER_1_TRIGGER", "apple-1", True, timestamp
            )
        self.assertEqual([1], self.actuator.extend_calls)

    def test_wrong_apple_at_selected_trigger_fails(self):
        self.controller.submit(self.request(), 1.0)
        self.controller.checkpoint(
            "CONVEYOR_PUSHER_1_TRIGGER", "apple-other", True, 2.0
        )
        self.assertEqual(SortStatus.FAILED, self.statuses[-1][1])
        self.assertEqual("APPLE_ID_MISMATCH", self.statuses[-1][3])

    def test_trigger_push_jam_and_home_timeouts(self):
        self.controller.submit(self.request(), 1.0)
        self.controller.tick(6.0)
        self.assertEqual("TRIGGER_TIMEOUT", self.statuses[-1][3])

        self.controller.submit(self.request(command_id="command-2"), 7.0)
        self.controller.checkpoint(
            "CONVEYOR_PUSHER_1_TRIGGER", "apple-1", True, 8.0
        )
        self.controller.tick(10.0)
        self.assertEqual("PUSH_TIMEOUT", self.statuses[-1][3])

        self.actuator.home[1] = True
        self.controller.submit(self.request(command_id="command-3"), 11.0)
        self.controller.checkpoint(
            "CONVEYOR_PUSHER_1_TRIGGER", "apple-1", False, 11.1
        )
        self.controller.checkpoint(
            "CONVEYOR_PUSHER_1_TRIGGER", "apple-1", True, 12.0
        )
        self.actuator.jammed = True
        self.controller.tick(12.1)
        self.assertEqual("JAM_DETECTED", self.statuses[-1][3])

        self.actuator.jammed = False
        self.actuator.home[1] = True
        self.controller.submit(self.request(command_id="command-4"), 13.0)
        self.controller.checkpoint(
            "CONVEYOR_PUSHER_1_TRIGGER", "apple-1", False, 13.1
        )
        self.controller.checkpoint(
            "CONVEYOR_PUSHER_1_TRIGGER", "apple-1", True, 14.0
        )
        self.actuator.extended[1] = True
        self.controller.tick(14.1)
        self.controller.tick(17.1)
        self.assertEqual("HOME_TIMEOUT", self.statuses[-1][3])

    def test_explicit_cancel_uses_cancelled_error(self):
        self.controller.submit(self.request(), 1.0)
        self.controller.cancel()

        self.assertEqual(SortStatus.CANCELLED, self.statuses[-1][1])
        self.assertEqual("CANCELLED", self.statuses[-1][3])

    def test_reset_cancels_and_clears_all_lifecycle_caches(self):
        request = self.request()
        self.controller.submit(request, 1.0)
        self.controller.reset()

        self.assertEqual(SortStatus.CANCELLED, self.statuses[-1][1])
        self.assertEqual("SIMULATION_RESET", self.statuses[-1][3])
        self.assertEqual({}, self.controller.command_cache)
        self.assertEqual(set(), self.controller.sorted_apples)
        self.assertIsNone(self.controller.active)


if __name__ == "__main__":
    unittest.main()
