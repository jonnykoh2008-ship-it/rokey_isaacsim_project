import unittest
from collections import deque
from types import SimpleNamespace
from unittest.mock import Mock

import numpy as np

from appleproj_interfaces.msg import HarvestTarget, PlanningScene, SimulationState
from geometry_msgs.msg import PoseStamped
from harvest_coordinator import HarvestCoordinator, PendingTarget
from harvest_route_planner import RoutePlanningError


class HarvestCoordinatorSynchronizationTest(unittest.TestCase):
    @staticmethod
    def make_coordinator():
        coordinator = HarvestCoordinator.__new__(HarvestCoordinator)
        coordinator.simulation_state = None
        coordinator.planning_scene = None
        coordinator.failed_target = None
        coordinator.execute_enabled = True
        coordinator.sample_count = 1
        coordinator.maximum_spread = 0.04
        coordinator.running = False
        coordinator.index = 0
        coordinator._sample_target_key = None
        coordinator._active_target_key = None
        coordinator._active_candidate = None
        coordinator._latest_target_stamps = {}
        coordinator._started_target_keys = set()
        coordinator.safety_stopped = False
        coordinator.safety_stop_reason = None
        coordinator.target_samples = {}
        coordinator.pending_targets = {}
        coordinator.retry_targets = {}
        coordinator.completed_target_keys = set()
        coordinator.failed_once_target_keys = set()
        coordinator.final_failed_target_keys = set()
        coordinator.target_max_age_sec = None
        coordinator.minimum_target_confidence = None
        coordinator.minimum_valid_depth_ratio = None
        coordinator.maximum_tf_time_error_sec = None
        coordinator.generation = 0
        coordinator.goal_handle = None
        coordinator.approach_orientation = None
        coordinator.target = None
        coordinator.samples = deque(maxlen=1)
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
        coordinator.queue_dispatch_timer = Mock()
        return coordinator

    @staticmethod
    def candidate(target_id, center):
        message = HarvestTarget()
        message.header.frame_id = "world"
        message.header.stamp.sec = 10
        message.target_id = target_id
        message.reset_id = 2
        message.scene_version = 3
        return PendingTarget(
            key=(2, target_id),
            message=message,
            center=np.asarray(center, dtype=float),
            stamp_ns=10_000_000_000,
        )

    @staticmethod
    def target_message(
        *,
        target_id="apple-1",
        stamp_sec=10,
        source_stamp_sec=None,
        frame_id="world",
        source_frame="base_camera",
        confidence=0.9,
        valid_depth_ratio=0.8,
        tf_time_error_sec=0.01,
    ):
        if source_stamp_sec is None:
            source_stamp_sec = stamp_sec
        return SimpleNamespace(
            header=SimpleNamespace(
                frame_id=frame_id,
                stamp=SimpleNamespace(sec=stamp_sec, nanosec=0),
            ),
            target_id=target_id,
            reset_id=2,
            scene_version=3,
            position=SimpleNamespace(x=0.8, y=0.4, z=1.2),
            source_point=SimpleNamespace(
                header=SimpleNamespace(
                    frame_id=source_frame,
                    stamp=SimpleNamespace(sec=source_stamp_sec, nanosec=0),
                ),
                point=SimpleNamespace(x=0.1, y=0.2, z=0.7),
            ),
            confidence=confidence,
            valid_depth_ratio=valid_depth_ratio,
            tf_time_error_sec=tf_time_error_sec,
        )

    @staticmethod
    def state(state, reset_id=2, scene_version=3):
        return SimpleNamespace(
            state=state,
            reset_id=reset_id,
            scene_version=scene_version,
            message="test",
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

    def test_harvest_target_contract_accepts_valid_message(self):
        coordinator = self.make_coordinator()

        self.assertIsNone(
            coordinator._validate_target(self.target_message())
        )

    def test_harvest_target_contract_rejects_unsynchronized_source_stamp(self):
        coordinator = self.make_coordinator()

        reason = coordinator._validate_target(
            self.target_message(source_stamp_sec=9)
        )

        self.assertIn("timestamp가 일치", reason)

    def test_harvest_target_contract_rejects_invalid_ranges(self):
        coordinator = self.make_coordinator()

        reason = coordinator._validate_target(
            self.target_message(confidence=1.1)
        )

        self.assertIn("confidence", reason)

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

    def test_approach_goal_keeps_path_generation_on_gpu_action_server(self):
        coordinator = self.make_coordinator()
        coordinator.simulation_state = self.state(SimulationState.PLAYING)
        scene = PlanningScene()
        scene.reset_id = 2
        scene.scene_version = 3
        scene.robot_base_pose.pose.position.x = 1.5
        scene.robot_base_pose.pose.position.y = 0.6
        scene.robot_base_pose.pose.position.z = 0.5
        coordinator.planning_scene = scene

        current_tcp = PoseStamped()
        current_tcp.pose.position.x = 1.5
        current_tcp.pose.position.y = 0.6
        current_tcp.pose.position.z = 2.0
        current_tcp.pose.orientation.z = np.sqrt(0.5)
        current_tcp.pose.orientation.w = np.sqrt(0.5)
        coordinator._current_tcp_pose = Mock(return_value=current_tcp)

        reset_id, scene_version, approach_orientation = (
            coordinator._prepare_approach_goal(
                np.array([0.8, 0.4, 1.2]),
            )
        )

        self.assertEqual((reset_id, scene_version), (2, 3))
        self.assertEqual(approach_orientation.shape, (4,))
        self.assertAlmostEqual(np.linalg.norm(approach_orientation), 1.0)
        coordinator._current_tcp_pose.assert_not_called()

    def test_accepted_approach_marks_target_as_started(self):
        coordinator = self.make_coordinator()
        coordinator.running = True
        coordinator.index = 0
        coordinator.generation = 4
        coordinator._active_target_key = (2, "apple-1")
        result_future = Mock()
        result_future.add_done_callback = Mock()
        handle = Mock(accepted=True)
        handle.get_result_async.return_value = result_future
        future = Mock()
        future.result.return_value = handle

        coordinator.on_goal_response(future, generation=4)

        self.assertIn((2, "apple-1"), coordinator._started_target_keys)
        self.assertIs(coordinator.goal_handle, handle)

    def test_reset_change_clears_started_target_keys(self):
        coordinator = self.make_coordinator()
        coordinator._started_target_keys.add((2, "apple-1"))
        coordinator.simulation_state = self.state(
            SimulationState.PLAYING, reset_id=2, scene_version=3
        )

        coordinator.on_state(
            self.state(SimulationState.READY, reset_id=3, scene_version=1)
        )

        self.assertEqual(coordinator._started_target_keys, set())

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

    def test_target_received_while_running_is_queued(self):
        coordinator = self.make_coordinator()
        coordinator.running = True
        coordinator.simulation_state = self.state(SimulationState.PLAYING)
        coordinator.planning_scene = self.scene()
        coordinator._planning_inputs_synchronized = Mock(return_value=True)

        coordinator.on_target(self.target_message(target_id="apple-2"))

        self.assertIn((2, "apple-2"), coordinator.pending_targets)
        self.assertTrue(coordinator.running)
        coordinator.queue_dispatch_timer.reset.assert_not_called()

    def test_new_target_ids_restart_batch_debounce(self):
        coordinator = self.make_coordinator()
        coordinator.simulation_state = self.state(SimulationState.PLAYING)
        coordinator.planning_scene = self.scene()
        coordinator._planning_inputs_synchronized = Mock(return_value=True)

        coordinator.on_target(self.target_message(target_id="apple-3"))
        coordinator.on_target(self.target_message(target_id="apple-1"))
        coordinator.on_target(self.target_message(target_id="apple-2"))

        self.assertEqual(coordinator.queue_dispatch_timer.reset.call_count, 3)
        self.assertFalse(coordinator.running)
        self.assertEqual(len(coordinator.pending_targets), 3)

    def test_batch_dispatch_selects_nearest_after_all_ids_arrive(self):
        coordinator = self.make_coordinator()
        coordinator.planning_scene = PlanningScene()
        far = self.candidate("apple-3", [1.5, 0.0, 0.0])
        near = self.candidate("apple-1", [0.6, 0.0, 0.0])
        middle = self.candidate("apple-2", [1.0, 0.0, 0.0])
        coordinator.pending_targets = {
            far.key: far,
            near.key: near,
            middle.key: middle,
        }
        coordinator._prepare_approach_goal = Mock(
            return_value=(2, 3, np.array([0.0, 0.0, 0.0, 1.0]))
        )
        coordinator.send_next = Mock()

        coordinator._dispatch_pending_targets()

        self.assertEqual(coordinator._active_target_key, near.key)
        self.assertIn(far.key, coordinator.pending_targets)
        self.assertIn(middle.key, coordinator.pending_targets)
        coordinator.queue_dispatch_timer.cancel.assert_called()

    def test_first_precontact_failure_moves_target_to_retry_queue(self):
        coordinator = self.make_coordinator()
        candidate = self.candidate("apple-1", [0.8, 0.1, 1.2])

        coordinator._defer_or_finish_failed_candidate(candidate, "RRT 실패")

        self.assertIn(candidate.key, coordinator.retry_targets)
        self.assertIn(candidate.key, coordinator.failed_once_target_keys)
        self.assertNotIn(candidate.key, coordinator.final_failed_target_keys)

    def test_second_precontact_failure_is_final(self):
        coordinator = self.make_coordinator()
        candidate = self.candidate("apple-1", [0.8, 0.1, 1.2])
        coordinator.failed_once_target_keys.add(candidate.key)

        coordinator._defer_or_finish_failed_candidate(candidate, "재시도 실패")

        self.assertNotIn(candidate.key, coordinator.retry_targets)
        self.assertIn(candidate.key, coordinator.final_failed_target_keys)

    def test_normal_queue_runs_before_retry_queue(self):
        coordinator = self.make_coordinator()
        coordinator.planning_scene = PlanningScene()
        normal = self.candidate("apple-2", [0.8, 0.1, 1.2])
        retry = self.candidate("apple-1", [0.7, 0.1, 1.2])
        coordinator.pending_targets[normal.key] = normal
        coordinator.retry_targets[retry.key] = retry
        coordinator._prepare_approach_goal = Mock(
            return_value=(2, 3, np.array([0.0, 0.0, 0.0, 1.0]))
        )
        coordinator.send_next = Mock()

        coordinator._start_next_target()

        self.assertEqual(coordinator._active_target_key, normal.key)
        self.assertIn(retry.key, coordinator.retry_targets)
        coordinator.send_next.assert_called_once_with()

    def test_normal_queue_selects_target_nearest_robot_base(self):
        coordinator = self.make_coordinator()
        coordinator.planning_scene = PlanningScene()
        far = self.candidate("apple-1", [1.5, 0.0, 0.0])
        near = self.candidate("apple-2", [0.6, 0.0, 0.0])
        coordinator.pending_targets[far.key] = far
        coordinator.pending_targets[near.key] = near
        coordinator._prepare_approach_goal = Mock(
            return_value=(2, 3, np.array([0.0, 0.0, 0.0, 1.0]))
        )
        coordinator.send_next = Mock()

        coordinator._start_next_target()

        self.assertEqual(coordinator._active_target_key, near.key)
        self.assertIn(far.key, coordinator.pending_targets)

    def test_postcontact_failure_stops_without_starting_next(self):
        coordinator = self.make_coordinator()
        candidate = self.candidate("apple-1", [0.8, 0.1, 1.2])
        queued = self.candidate("apple-2", [0.9, 0.1, 1.2])
        coordinator.running = True
        coordinator.target = PoseStamped()
        coordinator._active_candidate = candidate
        coordinator._active_target_key = candidate.key
        coordinator.pending_targets[queued.key] = queued
        coordinator._start_next_target = Mock()

        coordinator._handle_active_failure(
            "GRASP 이후 실패",
            allow_deferred_retry=False,
        )

        self.assertFalse(coordinator.running)
        self.assertTrue(coordinator.safety_stopped)
        self.assertEqual(coordinator.pending_targets, {})
        self.assertEqual(coordinator.retry_targets, {})
        self.assertIn(candidate.key, coordinator.final_failed_target_keys)
        coordinator._start_next_target.assert_not_called()
        coordinator._publish_status.assert_called_once_with(
            "SAFETY_STOPPED",
            False,
            0.0,
            "302:COLLISION_RISK",
            "접촉 이후 실패로 reset 전까지 연속 수확을 중단합니다: GRASP 이후 실패",
        )

    def test_safety_stop_rejects_new_target(self):
        coordinator = self.make_coordinator()
        coordinator.safety_stopped = True
        coordinator.safety_stop_reason = "운반 실패"

        coordinator.on_target(self.target_message(target_id="apple-2"))

        self.assertEqual(coordinator.pending_targets, {})
        coordinator._publish_status.assert_called_once()
        status = coordinator._publish_status.call_args.args
        self.assertEqual(status[0], "TARGET_RECEIVED")
        self.assertEqual(status[3], "302:COLLISION_RISK")
        self.assertIn("SAFETY_STOPPED", status[4])

    def test_safety_stop_is_released_only_by_reset_id_change(self):
        coordinator = self.make_coordinator()
        coordinator.safety_stopped = True
        coordinator.safety_stop_reason = "운반 실패"
        coordinator.simulation_state = self.state(
            SimulationState.PLAYING, reset_id=2, scene_version=3
        )

        coordinator.on_state(
            self.state(SimulationState.READY, reset_id=2, scene_version=4)
        )
        self.assertTrue(coordinator.safety_stopped)

        coordinator.on_state(
            self.state(SimulationState.READY, reset_id=3, scene_version=1)
        )
        self.assertFalse(coordinator.safety_stopped)
        self.assertIsNone(coordinator.safety_stop_reason)


if __name__ == "__main__":
    unittest.main()
