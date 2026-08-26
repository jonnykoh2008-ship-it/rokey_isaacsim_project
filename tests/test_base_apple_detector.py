import unittest
from types import SimpleNamespace
from unittest.mock import Mock

import numpy as np
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import CameraInfo, Image

from appleproj_interfaces.msg import HarvestPerceptionStatus, SimulationState
from base_apple_detector import (
    BaseAppleDetector,
    TARGET_QOS,
    validate_robot_id,
)


class BaseAppleDetectorConfigurationTest(unittest.TestCase):
    @staticmethod
    def image_with_frame(frame_id):
        message = Image()
        message.header.frame_id = frame_id
        return message

    @staticmethod
    def camera_info_with_frame(frame_id):
        message = CameraInfo()
        message.header.frame_id = frame_id
        return message

    @staticmethod
    def make_detector():
        detector = BaseAppleDetector.__new__(BaseAppleDetector)
        detector.robot_id = "robot_01"
        detector.camera_frame = "base_camera"
        return detector

    def test_robot_id_requires_an_approved_explicit_value(self):
        self.assertEqual(validate_robot_id(" robot_01 "), "robot_01")
        self.assertEqual(validate_robot_id("robot_02"), "robot_02")
        for invalid in ("", "robot_03", None):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    validate_robot_id(invalid)

    def test_matching_rgb_depth_and_camera_info_frames_are_accepted(self):
        detector = self.make_detector()
        error = detector.validate_input_frames(
            self.image_with_frame("base_camera"),
            self.image_with_frame("base_camera"),
            self.camera_info_with_frame("base_camera"),
        )
        self.assertIsNone(error)

    def test_cross_camera_input_frames_are_rejected(self):
        detector = self.make_detector()
        status, message = detector.validate_input_frames(
            self.image_with_frame("base_camera"),
            self.image_with_frame("other_camera"),
            self.camera_info_with_frame("base_camera"),
        )
        self.assertEqual(
            status, HarvestPerceptionStatus.INPUT_NOT_SYNCHRONIZED
        )
        self.assertIn("frame 불일치", message)

    def test_unexpected_profile_camera_frame_is_rejected(self):
        detector = self.make_detector()
        status, message = detector.validate_input_frames(
            self.image_with_frame("base_rsd455_02"),
            self.image_with_frame("base_rsd455_02"),
            self.camera_info_with_frame("base_rsd455_02"),
        )
        self.assertEqual(status, HarvestPerceptionStatus.TF_UNAVAILABLE)
        self.assertIn("expected=base_camera", message)

    def test_empty_camera_frame_is_not_replaced_with_legacy_default(self):
        detector = self.make_detector()
        rgb = self.image_with_frame("")
        with self.assertRaises(ValueError):
            detector.make_camera_pose(rgb, np.zeros(3))


class BaseAppleDetectorTrackingTest(unittest.TestCase):
    @staticmethod
    def make_detector():
        detector = BaseAppleDetector.__new__(BaseAppleDetector)
        detector.tracking_max_distance_m = 0.100
        detector.tracks = {}
        detector.tracks_initialized = False
        detector.next_track_index = 1
        detector.last_published_target_ids = ()
        detector.camera_info = None
        detector.last_status_publish_ns_by_key = {}
        return detector

    @staticmethod
    def candidate(world_xyz, camera_xyz=None):
        if camera_xyz is None:
            camera_xyz = world_xyz
        return {
            "world_position": np.asarray(world_xyz, dtype=float),
            "center_point": np.asarray(camera_xyz, dtype=float),
            "diagnostic": {"track_id": None, "reason": "accepted"},
        }

    def test_initial_ids_follow_robot_distance_not_contour_order(self):
        detector = self.make_detector()
        candidates = [
            self.candidate([0.8, 0.0, 0.0]),
            self.candidate([0.2, 0.0, 0.0]),
            self.candidate([0.5, 0.0, 0.0]),
        ]

        assignments = detector.initialize_tracks(candidates, np.zeros(3))

        self.assertEqual(
            [target_id for target_id, _candidate in assignments],
            ["apple_001", "apple_002", "apple_003"],
        )
        self.assertIs(assignments[0][1], candidates[1])
        self.assertIs(assignments[1][1], candidates[2])
        self.assertIs(assignments[2][1], candidates[0])

    def test_equal_robot_distance_uses_world_xyz_tie_break(self):
        detector = self.make_detector()
        candidates = [
            self.candidate([1.0, 0.5, 0.0]),
            self.candidate([1.0, -0.5, 0.0]),
        ]

        assignments = detector.initialize_tracks(candidates, np.zeros(3))

        self.assertIs(assignments[0][1], candidates[1])
        self.assertIs(assignments[1][1], candidates[0])

    def test_reordered_candidates_keep_ids_by_nearest_world_position(self):
        detector = self.make_detector()
        detector.initialize_tracks(
            [
                self.candidate([0.0, 0.0, 0.0]),
                self.candidate([0.3, 0.0, 0.0]),
                self.candidate([0.6, 0.0, 0.0]),
            ],
            np.zeros(3),
        )
        reordered = [
            self.candidate([0.61, 0.0, 0.0]),
            self.candidate([0.01, 0.0, 0.0]),
            self.candidate([0.31, 0.0, 0.0]),
        ]

        assignments = detector.associate_tracks(reordered)

        self.assertEqual(
            [(target_id, candidate["world_position"][0]) for target_id, candidate in assignments],
            [
                ("apple_001", 0.01),
                ("apple_002", 0.31),
                ("apple_003", 0.61),
            ],
        )

    def test_out_of_gate_candidate_does_not_create_new_id(self):
        detector = self.make_detector()
        detector.initialize_tracks(
            [self.candidate([0.0, 0.0, 0.0])], np.zeros(3)
        )
        next_index = detector.next_track_index

        assignments = detector.associate_tracks(
            [self.candidate([0.101, 0.0, 0.0])]
        )

        self.assertEqual(assignments, [])
        self.assertEqual(set(detector.tracks), {"apple_001"})
        self.assertEqual(detector.next_track_index, next_index)

    def test_one_candidate_is_not_assigned_to_two_tracks(self):
        detector = self.make_detector()
        detector.initialize_tracks(
            [
                self.candidate([0.0, 0.0, 0.0]),
                self.candidate([0.08, 0.0, 0.0]),
            ],
            np.zeros(3),
        )
        current = self.candidate([0.04, 0.0, 0.0])

        assignments = detector.associate_tracks([current])

        self.assertEqual(len(assignments), 1)
        self.assertEqual(len({id(candidate) for _target_id, candidate in assignments}), 1)
        self.assertEqual(current["diagnostic"]["track_id"], assignments[0][0])

    def test_missing_track_is_retained_without_publication(self):
        detector = self.make_detector()
        detector.initialize_tracks(
            [
                self.candidate([0.0, 0.0, 0.0]),
                self.candidate([0.3, 0.0, 0.0]),
            ],
            np.zeros(3),
        )

        assignments = detector.associate_tracks(
            [self.candidate([0.01, 0.0, 0.0])]
        )

        self.assertEqual([target_id for target_id, _ in assignments], ["apple_001"])
        self.assertEqual(set(detector.tracks), {"apple_001", "apple_002"})
        np.testing.assert_allclose(
            detector.tracks["apple_002"]["last_world_position"],
            [0.3, 0.0, 0.0],
        )

    def test_reset_clears_state_and_restarts_id_sequence(self):
        detector = self.make_detector()
        detector.initialize_tracks(
            [self.candidate([0.0, 0.0, 0.0])], np.zeros(3)
        )
        detector.camera_info = object()
        detector.latest_rgb = object()
        detector.latest_depth = object()
        detector.last_processed_rgb_stamp = 123
        detector.last_published_target_ids = ("apple_001",)
        detector.last_detection_log_ns = 10
        detector.last_tf_warning_ns = 20
        detector.last_status_code = 1
        detector.last_status_publish_ns = 30
        detector.last_status_publish_ns_by_key = {(0, "apple_001"): 30}

        detector.reset_tracking_state()
        assignments = detector.initialize_tracks(
            [self.candidate([1.0, 0.0, 0.0])], np.zeros(3)
        )

        self.assertEqual([target_id for target_id, _ in assignments], ["apple_001"])
        self.assertIsNone(detector.camera_info)
        self.assertIsNone(detector.latest_rgb)
        self.assertIsNone(detector.latest_depth)
        self.assertEqual(detector.last_processed_rgb_stamp, -1)
        self.assertEqual(detector.last_published_target_ids, ())
        self.assertEqual(detector.last_detection_log_ns, -1)
        self.assertEqual(detector.last_status_code, None)
        self.assertEqual(detector.last_status_publish_ns_by_key, {})

    def test_simulation_reset_callback_invokes_full_reset(self):
        detector = self.make_detector()
        detector.simulation_state = SimpleNamespace(reset_id=7)
        detector.reset_tracking_state = Mock()
        detector.get_logger = Mock(return_value=Mock())

        detector.simulation_state_callback(SimpleNamespace(reset_id=8))

        detector.reset_tracking_state.assert_called_once_with()

    def test_target_qos_keeps_ten_messages(self):
        self.assertEqual(TARGET_QOS.depth, 10)


class BaseAppleDetectorSynchronizationTest(unittest.TestCase):
    @staticmethod
    def image_at(nanoseconds):
        message = Image()
        message.header.stamp.sec = nanoseconds // 1_000_000_000
        message.header.stamp.nanosec = nanoseconds % 1_000_000_000
        return message

    @staticmethod
    def make_detector():
        detector = BaseAppleDetector.__new__(BaseAppleDetector)
        detector.camera_info = object()
        detector.latest_rgb = None
        detector.latest_depth = None
        detector.last_processed_rgb_stamp = -1
        detector.maximum_sync_error_ns = 80_000_000
        detector.process_rgbd = Mock()
        detector.publish_perception_status = Mock()
        detector.get_logger = Mock(return_value=Mock())
        return detector

    def test_delayed_depth_matches_waiting_rgb_instead_of_latest_rgb(self):
        detector = self.make_detector()
        waiting_rgb = self.image_at(1_000_000_000)
        newer_rgb = self.image_at(2_000_000_000)
        delayed_depth = self.image_at(1_000_000_000)

        detector.rgb_callback(waiting_rgb)
        detector.rgb_callback(newer_rgb)
        detector.depth_callback(delayed_depth)

        detector.process_rgbd.assert_called_once_with(
            waiting_rgb, delayed_depth, detector.camera_info
        )
        self.assertIsNone(detector.latest_rgb)
        self.assertIsNone(detector.latest_depth)

    def test_stale_message_is_discarded_and_next_pair_recovers(self):
        detector = self.make_detector()
        stale_rgb = self.image_at(1_000_000_000)
        depth = self.image_at(2_000_000_000)
        matching_rgb = self.image_at(2_000_000_000)

        detector.rgb_callback(stale_rgb)
        detector.depth_callback(depth)

        self.assertIsNone(detector.latest_rgb)
        self.assertIs(detector.latest_depth, depth)
        detector.publish_perception_status.assert_called_once()

        detector.rgb_callback(matching_rgb)

        detector.process_rgbd.assert_called_once_with(
            matching_rgb, depth, detector.camera_info
        )

    def test_processed_pair_is_not_processed_again(self):
        detector = self.make_detector()
        rgb = self.image_at(3_000_000_000)
        depth = self.image_at(3_000_000_000)

        detector.rgb_callback(rgb)
        detector.depth_callback(depth)
        detector.rgb_callback(rgb)
        detector.depth_callback(depth)

        detector.process_rgbd.assert_called_once_with(
            rgb, depth, detector.camera_info
        )
        self.assertIsNone(detector.latest_rgb)
        self.assertIsNone(detector.latest_depth)


class BaseAppleDetectorPublicationTest(unittest.TestCase):
    @staticmethod
    def make_detector():
        detector = BaseAppleDetector.__new__(BaseAppleDetector)
        state = SimulationState()
        state.state = SimulationState.PLAYING
        state.reset_id = 5
        state.scene_version = 9
        detector.simulation_state = state
        detector.target_publisher = Mock()
        detector.publish_perception_status = Mock()
        return detector

    @staticmethod
    def messages():
        rgb = Image()
        rgb.header.stamp.sec = 12
        rgb.header.stamp.nanosec = 345
        rgb.header.frame_id = "base_camera"

        camera_pose = PoseStamped()
        camera_pose.header = rgb.header
        camera_pose.pose.position.x = 0.1
        camera_pose.pose.position.y = 0.2
        camera_pose.pose.position.z = 0.8

        world_pose = PoseStamped()
        world_pose.header.stamp = rgb.header.stamp
        world_pose.header.frame_id = "world"
        world_pose.pose.position.x = 0.8
        world_pose.pose.position.y = 0.4
        world_pose.pose.position.z = 1.2
        return rgb, camera_pose, world_pose

    @classmethod
    def make_three_contour_detector(cls, robot_base_result):
        detector = cls.make_detector()
        detector.tracking_max_distance_m = 0.100
        detector.tracks = {}
        detector.tracks_initialized = False
        detector.next_track_index = 1
        detector.last_published_target_ids = ()
        detector.last_detection_log_ns = -1
        detector.apple_radius_m = 0.04
        detector.minimum_contour_confidence = None
        detector.robot_id = "robot_01"
        detector.camera_frame = "base_camera"
        detector.robot_base_frame = "base_link"
        detector.bridge = Mock()
        detector.bridge.imgmsg_to_cv2.return_value = np.zeros(
            (64, 64, 3), dtype=np.uint8
        )
        detector.depth_in_meters = Mock(
            return_value=np.ones((64, 64), dtype=np.float32)
        )
        contours = [object(), object(), object()]
        detector.find_apple_contours = Mock(return_value=(contours, None))
        detector.contour_shape_metrics = Mock(
            return_value=(100.0, 0.9, 0.9, 0.9)
        )
        detector.contour_center = Mock(
            side_effect=[(10.0, 10.0), (20.0, 20.0), (30.0, 30.0)]
        )
        detector.robust_depth = Mock(return_value=(1.0, 0.8))
        detector.deproject = Mock(
            side_effect=[
                np.array([0.8, 0.4, 1.2]),
                np.array([0.4, 0.8, 1.0]),
                np.array([0.4, 0.2, 1.4]),
            ]
        )
        detector.surface_point_to_center = Mock(
            side_effect=lambda point, _radius: point
        )

        def transform_to_world(camera_pose):
            world_pose = PoseStamped()
            world_pose.header.stamp = camera_pose.header.stamp
            world_pose.header.frame_id = "world"
            world_pose.pose.position = camera_pose.pose.position
            return world_pose, 0.0

        detector.transform_to_world = transform_to_world
        detector.lookup_robot_base_world = Mock(return_value=robot_base_result)
        detector.camera_pose_publisher = Mock()
        detector.draw_candidate_diagnostics = Mock()
        detector.publish_debug_image = Mock()
        detector.show_debug = Mock()
        detector.get_clock = Mock(
            return_value=SimpleNamespace(
                now=Mock(return_value=SimpleNamespace(nanoseconds=1_000_000_000))
            )
        )
        detector.get_logger = Mock(return_value=Mock())

        rgb, _camera_pose, _world_pose = cls.messages()
        depth = Image()
        depth.header = rgb.header
        camera_info = CameraInfo()
        camera_info.header = rgb.header
        return detector, rgb, depth, camera_info

    def test_three_targets_preserve_frame_metadata(self):
        detector = self.make_detector()
        rgb, camera_pose, world_pose = self.messages()

        for target_id in ("apple_001", "apple_002", "apple_003"):
            published = detector.publish_harvest_target(
                target_id,
                rgb,
                camera_pose,
                world_pose,
                confidence=0.9,
                valid_depth_ratio=0.8,
                tf_time_error_sec=0.01,
            )
            self.assertTrue(published)

        targets = [call.args[0] for call in detector.target_publisher.publish.call_args_list]
        self.assertEqual(
            [target.target_id for target in targets],
            ["apple_001", "apple_002", "apple_003"],
        )
        self.assertTrue(all(target.header.frame_id == "world" for target in targets))
        self.assertTrue(all(target.header.stamp.sec == 12 for target in targets))
        self.assertTrue(all(target.header.stamp.nanosec == 345 for target in targets))
        self.assertTrue(all(target.source_point.header.stamp.sec == 12 for target in targets))
        self.assertTrue(all(target.reset_id == 5 for target in targets))
        self.assertTrue(all(target.scene_version == 9 for target in targets))

    def test_three_contours_are_initialized_and_published_in_one_frame(self):
        detector, rgb, depth, camera_info = self.make_three_contour_detector(
            (np.zeros(3), 0.0)
        )
        detector.process_rgbd(rgb, depth, camera_info)

        targets = [call.args[0] for call in detector.target_publisher.publish.call_args_list]
        self.assertEqual(
            [target.target_id for target in targets],
            ["apple_001", "apple_002", "apple_003"],
        )
        self.assertEqual(
            detector.last_published_target_ids,
            ("apple_001", "apple_002", "apple_003"),
        )
        self.assertAlmostEqual(targets[0].position.x, 0.4)
        self.assertAlmostEqual(targets[0].position.y, 0.8)
        self.assertAlmostEqual(targets[1].position.x, 0.4)
        self.assertAlmostEqual(targets[1].position.y, 0.2)
        self.assertAlmostEqual(targets[2].position.x, 0.8)
        self.assertAlmostEqual(targets[2].position.y, 0.4)

    def test_missing_robot_base_tf_holds_initial_id_creation(self):
        detector, rgb, depth, camera_info = self.make_three_contour_detector(
            (None, np.nan)
        )

        detector.process_rgbd(rgb, depth, camera_info)

        self.assertFalse(detector.tracks_initialized)
        detector.target_publisher.publish.assert_not_called()
        detector.publish_perception_status.assert_called_once()
        status_call = detector.publish_perception_status.call_args
        self.assertEqual(
            status_call.args[1], HarvestPerceptionStatus.TF_UNAVAILABLE
        )


class BaseAppleDetectorStatusThrottleTest(unittest.TestCase):
    def test_ok_status_is_throttled_per_target_id(self):
        detector = BaseAppleDetector.__new__(BaseAppleDetector)
        detector.simulation_state = None
        detector.perception_status_publisher = Mock()
        detector.last_status_code = None
        detector.last_status_publish_ns = -1
        detector.last_status_publish_ns_by_key = {}
        detector.get_clock = Mock(
            return_value=SimpleNamespace(
                now=Mock(return_value=SimpleNamespace(nanoseconds=1_000_000_000))
            )
        )
        source = Image()
        source.header.frame_id = "base_camera"

        detector.publish_perception_status(
            source, HarvestPerceptionStatus.OK, target_id="apple_001"
        )
        detector.publish_perception_status(
            source, HarvestPerceptionStatus.OK, target_id="apple_002"
        )
        detector.publish_perception_status(
            source, HarvestPerceptionStatus.OK, target_id="apple_001"
        )

        published = [
            call.args[0]
            for call in detector.perception_status_publisher.publish.call_args_list
        ]
        self.assertEqual(
            [message.target_id for message in published],
            ["apple_001", "apple_002"],
        )


if __name__ == "__main__":
    unittest.main()
