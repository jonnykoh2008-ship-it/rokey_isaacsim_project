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
        coordinator.control_to_tcp_rotation = np.eye(3)
        coordinator.control_to_tcp_translation = np.zeros(3)
        coordinator._last_calibration_failure = None
        coordinator.tf_buffer = Mock()
        coordinator.tf_buffer.all_frames_as_string.return_value = "world -> link_6"
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

    def test_execute_waits_for_tcp_calibration(self):
        coordinator = self.make_coordinator()
        coordinator.simulation_state = self.state(SimulationState.READY)
        coordinator.planning_scene = self.scene()
        coordinator.control_to_tcp_rotation = None
        coordinator.control_to_tcp_translation = None

        self.assertFalse(coordinator._planning_inputs_synchronized())

    def test_dry_run_does_not_require_tcp_calibration(self):
        coordinator = self.make_coordinator()
        coordinator.execute_enabled = False
        coordinator.simulation_state = self.state(SimulationState.READY)
        coordinator.planning_scene = self.scene()
        coordinator.control_to_tcp_rotation = None
        coordinator.control_to_tcp_translation = None

        self.assertTrue(coordinator._planning_inputs_synchronized())

    @staticmethod
    def calibration_scene():
        scene = PlanningScene()
        scene.header.frame_id = "world"
        scene.robot_tcp_pose.header.frame_id = "world"
        scene.robot_tcp_pose.pose.position.x = 0.3
        scene.robot_tcp_pose.pose.position.y = 0.4
        scene.robot_tcp_pose.pose.position.z = 0.5
        scene.robot_tcp_pose.pose.orientation.w = 1.0
        return scene

    def test_calibration_uses_scene_stamp_when_available(self):
        coordinator = self.make_coordinator()
        coordinator.control_to_tcp_rotation = None
        coordinator.control_to_tcp_translation = None
        coordinator._lookup_control_frame = Mock(
            return_value=(np.eye(3), np.array([0.1, 0.1, 0.1]))
        )

        self.assertTrue(
            coordinator._calibrate_control_frame_to_tcp(self.calibration_scene())
        )
        np.testing.assert_allclose(
            coordinator.control_to_tcp_translation, [0.2, 0.3, 0.4]
        )
        coordinator._lookup_control_frame.assert_called_once()

    def test_calibration_falls_back_to_latest_tf_only_when_idle(self):
        coordinator = self.make_coordinator()
        coordinator.simulation_state = self.state(SimulationState.PLAYING)
        coordinator.control_to_tcp_rotation = None
        coordinator.control_to_tcp_translation = None
        coordinator._lookup_control_frame = Mock(
            side_effect=[
                RoutePlanningError("stamp predates buffer"),
                (np.eye(3), np.array([0.1, 0.1, 0.1])),
            ]
        )

        self.assertTrue(
            coordinator._calibrate_control_frame_to_tcp(self.calibration_scene())
        )
        self.assertEqual(coordinator._lookup_control_frame.call_count, 2)
        coordinator.get_logger.return_value.warning.assert_called_once()

    def test_calibration_does_not_fall_back_while_running(self):
        coordinator = self.make_coordinator()
        coordinator.running = True
        coordinator.simulation_state = self.state(SimulationState.PLAYING)
        coordinator.control_to_tcp_rotation = None
        coordinator.control_to_tcp_translation = None
        coordinator._lookup_control_frame = Mock(
            side_effect=RoutePlanningError("stamp predates buffer")
        )

        self.assertFalse(
            coordinator._calibrate_control_frame_to_tcp(self.calibration_scene())
        )
        coordinator._lookup_control_frame.assert_called_once()
        coordinator.tf_buffer.all_frames_as_string.assert_called_once_with()

    def test_successful_calibration_is_not_recomputed(self):
        coordinator = self.make_coordinator()
        coordinator._lookup_control_frame = Mock()

        self.assertTrue(
            coordinator._calibrate_control_frame_to_tcp(self.calibration_scene())
        )
        coordinator._lookup_control_frame.assert_not_called()

    def test_retry_timer_retries_tcp_calibration_for_matching_scene(self):
        coordinator = self.make_coordinator()
        coordinator.simulation_state = self.state(SimulationState.READY)
        coordinator.planning_scene = self.scene()
        coordinator.control_to_tcp_rotation = None
        coordinator.control_to_tcp_translation = None
        coordinator._calibrate_control_frame_to_tcp = Mock(return_value=False)

        coordinator._retry_snapshot()

        coordinator.request_snapshot.assert_not_called()
        coordinator._calibrate_control_frame_to_tcp.assert_called_once_with(
            coordinator.planning_scene
        )

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
