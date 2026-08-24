import unittest
from types import SimpleNamespace
from unittest.mock import Mock

import numpy as np

from appleproj_interfaces.msg import PlanningScene, SimulationState
from harvest_coordinator import HarvestCoordinator
from harvest_route_planner import RoutePlanningError


class HarvestCoordinatorSynchronizationTest(unittest.TestCase):
    @staticmethod
    def make_coordinator():
        coordinator = HarvestCoordinator.__new__(HarvestCoordinator)
        coordinator.simulation_state = None
        coordinator.planning_scene = None
        coordinator.failed_target = None
        coordinator.execute_enabled = True
        coordinator.running = False
        coordinator._last_tcp_lookup_failure = None
        coordinator.tf_buffer = Mock()
        coordinator.tf_buffer.all_frames_as_string.return_value = "world -> palm"
        coordinator._lookup_tcp_frame = Mock(
            return_value=(np.eye(3), np.zeros(3))
        )
        coordinator.get_clock = Mock(
            return_value=SimpleNamespace(
                now=Mock(
                    return_value=SimpleNamespace(
                        to_msg=Mock(return_value=SimpleNamespace())
                    )
                )
            )
        )
        coordinator.request_snapshot = Mock()
        coordinator._publish_status = Mock()
        coordinator.get_logger = Mock(return_value=Mock())
        return coordinator

    @staticmethod
    def state(state, reset_id=2, scene_version=3):
        return SimpleNamespace(
            state=state,
            reset_id=reset_id,
            scene_version=scene_version,
        )

    @staticmethod
    def scene(reset_id=2, scene_version=3):
        return SimpleNamespace(
            reset_id=reset_id,
            scene_version=scene_version,
        )

    def test_waits_until_simulation_is_ready_or_playing(self):
        coordinator = self.make_coordinator()

        self.assertFalse(coordinator._planning_inputs_synchronized())
        for state in (SimulationState.INITIALIZING, SimulationState.PAUSED):
            coordinator.simulation_state = self.state(state)
            coordinator.planning_scene = self.scene()
            self.assertFalse(coordinator._planning_inputs_synchronized())

        coordinator.request_snapshot.assert_not_called()

    def test_requests_snapshot_when_ready_without_scene(self):
        coordinator = self.make_coordinator()
        coordinator.simulation_state = self.state(SimulationState.READY)

        self.assertFalse(coordinator._planning_inputs_synchronized())
        coordinator.request_snapshot.assert_called_once_with()

    def test_rejects_stale_scene_and_requests_snapshot(self):
        coordinator = self.make_coordinator()
        coordinator.simulation_state = self.state(SimulationState.PLAYING)
        coordinator.planning_scene = self.scene(scene_version=2)

        self.assertFalse(coordinator._planning_inputs_synchronized())
        self.assertIsNone(coordinator.planning_scene)
        coordinator.request_snapshot.assert_called_once_with()

    def test_accepts_matching_scene_when_ready(self):
        coordinator = self.make_coordinator()
        coordinator.simulation_state = self.state(SimulationState.READY)
        coordinator.planning_scene = self.scene()

        self.assertTrue(coordinator._planning_inputs_synchronized())
        coordinator.request_snapshot.assert_not_called()

    def test_execute_waits_until_palm_tf_is_available(self):
        coordinator = self.make_coordinator()
        coordinator.simulation_state = self.state(SimulationState.READY)
        coordinator.planning_scene = self.scene()
        coordinator._lookup_tcp_frame = Mock(
            side_effect=RoutePlanningError("palm TF is unavailable")
        )

        self.assertFalse(coordinator._planning_inputs_synchronized())
        coordinator.tf_buffer.all_frames_as_string.assert_called_once_with()

    def test_dry_run_does_not_require_palm_tf(self):
        coordinator = self.make_coordinator()
        coordinator.execute_enabled = False
        coordinator.simulation_state = self.state(SimulationState.READY)
        coordinator.planning_scene = self.scene()
        coordinator._lookup_tcp_frame = Mock(
            side_effect=RoutePlanningError("palm TF is unavailable")
        )

        self.assertTrue(coordinator._planning_inputs_synchronized())
        coordinator._lookup_tcp_frame.assert_not_called()

    def test_current_tcp_pose_uses_palm_local_y_offset(self):
        coordinator = self.make_coordinator()
        coordinator._lookup_tcp_frame = Mock(
            return_value=(np.eye(3), np.array([0.1, 0.2, 0.3]))
        )

        pose = coordinator._current_tcp_pose()

        np.testing.assert_allclose(
            [pose.pose.position.x, pose.pose.position.y, pose.pose.position.z],
            [0.1, 0.2908, 0.3],
        )
        np.testing.assert_allclose(
            [
                pose.pose.orientation.x,
                pose.pose.orientation.y,
                pose.pose.orientation.z,
                pose.pose.orientation.w,
            ],
            [0.0, 0.0, 0.0, 1.0],
        )

    def test_current_tcp_pose_rotates_palm_local_y_offset(self):
        coordinator = self.make_coordinator()
        palm_rotation = np.array(
            [
                [0.0, -1.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0],
            ]
        )
        coordinator._lookup_tcp_frame = Mock(
            return_value=(palm_rotation, np.zeros(3))
        )

        pose = coordinator._current_tcp_pose()

        np.testing.assert_allclose(
            [pose.pose.position.x, pose.pose.position.y, pose.pose.position.z],
            [-0.0908, 0.0, 0.0],
        )
        np.testing.assert_allclose(
            [
                pose.pose.orientation.x,
                pose.pose.orientation.y,
                pose.pose.orientation.z,
                pose.pose.orientation.w,
            ],
            [0.0, 0.0, np.sqrt(0.5), np.sqrt(0.5)],
        )

    def test_tcp_lookup_failure_is_logged_once(self):
        coordinator = self.make_coordinator()
        coordinator._lookup_tcp_frame = Mock(
            side_effect=RoutePlanningError("palm TF is unavailable")
        )

        self.assertFalse(coordinator._tcp_pose_available())
        self.assertFalse(coordinator._tcp_pose_available())
        self.assertEqual(coordinator.get_logger.return_value.warning.call_count, 1)

    def test_retry_timer_checks_palm_tf_for_matching_scene(self):
        coordinator = self.make_coordinator()
        coordinator.simulation_state = self.state(SimulationState.READY)
        coordinator.planning_scene = self.scene()
        coordinator._lookup_tcp_frame = Mock(
            side_effect=RoutePlanningError("palm TF is unavailable")
        )

        coordinator._retry_snapshot()

        coordinator.request_snapshot.assert_not_called()
        coordinator._lookup_tcp_frame.assert_called_once()

    def test_simulation_reset_does_not_latch_failed_target(self):
        coordinator = self.make_coordinator()
        center = np.array([0.8, 0.1, 1.6])

        coordinator._report_plan_failure(
            center,
            RoutePlanningError("simulation state가 READY 상태가 아닙니다."),
        )

        self.assertIsNone(coordinator.failed_target)
        coordinator._publish_status.assert_called_once_with(
            "PRE_GRASP_PLANNING",
            False,
            0.0,
            "308:SIMULATION_RESET",
            "simulation state가 READY 상태가 아닙니다.",
        )

    def test_collision_failure_latches_failed_target(self):
        coordinator = self.make_coordinator()
        center = np.array([0.8, 0.1, 1.6])

        coordinator._report_plan_failure(
            center,
            RoutePlanningError("접근 경로 충돌"),
        )

        np.testing.assert_allclose(coordinator.failed_target, center)
        coordinator._publish_status.assert_called_once_with(
            "PRE_GRASP_PLANNING",
            False,
            0.0,
            "302:COLLISION_RISK",
            "접근 경로 충돌",
        )


if __name__ == "__main__":
    unittest.main()
