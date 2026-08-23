import unittest
from types import SimpleNamespace
from unittest.mock import Mock

import numpy as np

from appleproj_interfaces.msg import SimulationState
from harvest_coordinator import HarvestCoordinator
from harvest_route_planner import RoutePlanningError


class HarvestCoordinatorSynchronizationTest(unittest.TestCase):
    @staticmethod
    def make_coordinator():
        coordinator = HarvestCoordinator.__new__(HarvestCoordinator)
        coordinator.simulation_state = None
        coordinator.planning_scene = None
        coordinator.failed_target = None
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
