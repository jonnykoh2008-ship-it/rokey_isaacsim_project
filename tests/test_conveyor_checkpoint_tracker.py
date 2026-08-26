import unittest

import numpy as np

from conveyor_checkpoint_tracker import (
    INSPECTION_CHECKPOINT_ID,
    ConveyorBounds,
    InspectionCheckpointTracker,
    LandingConfig,
    LandingObservation,
    LandingTracker,
)


class ConveyorCheckpointTrackerTest(unittest.TestCase):
    def setUp(self):
        self.bounds = ConveyorBounds(
            np.array([0.0, -0.5, 0.0]),
            np.array([2.0, 0.5, 0.1]),
            travel_axis=0,
        )

    def observation(self, x, y=0.0, velocity=(0.3, 0.0, 0.0), contact=True):
        return LandingObservation(
            center=np.array([x, y, 0.15]),
            linear_velocity=np.array(velocity),
            belt_contact=contact,
            gripper_attached=False,
        )

    def test_landing_regions_split_length_and_use_center_width_40_percent(self):
        self.assertTrue(self.bounds.in_landing_region("robot_01", [0.5, 0.19, 0.15]))
        self.assertFalse(self.bounds.in_landing_region("robot_01", [1.5, 0.0, 0.15]))
        self.assertTrue(self.bounds.in_landing_region("robot_02", [1.5, -0.19, 0.15]))
        self.assertFalse(self.bounds.in_landing_region("robot_02", [1.5, 0.21, 0.15]))

    def test_landing_requires_contact_detachment_velocity_and_stable_dwell(self):
        tracker = LandingTracker(self.bounds, belt_speed_mps=0.3)
        tracker.start("robot_01", "reservation-1", "apple_001", "/apple/1", 1.0)

        self.assertIsNone(tracker.update(self.observation(0.5, contact=False), 1.1))
        attached = self.observation(0.5)
        attached = LandingObservation(
            attached.center, attached.linear_velocity, True, True
        )
        self.assertIsNone(tracker.update(attached, 1.2))
        self.assertIsNone(tracker.update(self.observation(0.5), 1.3))
        result = tracker.update(self.observation(0.6), 1.6)

        self.assertEqual(LandingTracker.CONFIRMED, result.state)
        self.assertEqual("apple_001", result.apple_id)

    def test_landing_timeout_uses_supplied_simulation_time(self):
        tracker = LandingTracker(
            self.bounds,
            belt_speed_mps=0.3,
            config=LandingConfig(timeout_s=2.0),
        )
        tracker.start("robot_02", "reservation-2", "apple_004", "/apple/4", 5.0)

        self.assertIsNone(tracker.update(self.observation(1.5, contact=False), 5.0))
        self.assertIsNone(tracker.update(self.observation(1.5, contact=False), 5.0))
        result = tracker.update(self.observation(1.5, contact=False), 7.0)

        self.assertEqual(LandingTracker.TIMEOUT, result.state)

    def test_inspection_roi_emits_one_enter_and_exit(self):
        records = []
        tracker = InspectionCheckpointTracker(
            self.bounds, (0.25, 0.75), records.append
        )
        tracker.bind_apple("apple_001", "/apple/1")

        tracker.update({"/apple/1": np.array([0.2, 0.0, 0.15])})
        tracker.update({"/apple/1": np.array([0.6, 0.0, 0.15])})
        tracker.update({"/apple/1": np.array([0.7, 0.0, 0.15])})
        tracker.update({"/apple/1": np.array([1.8, 0.0, 0.15])})

        self.assertEqual(2, len(records))
        self.assertEqual(INSPECTION_CHECKPOINT_ID, records[0].checkpoint_id)
        self.assertTrue(records[0].entered)
        self.assertFalse(records[1].entered)

    def test_binding_rejects_id_or_prim_conflicts(self):
        tracker = InspectionCheckpointTracker(self.bounds, (0.2, 0.8), lambda _x: None)
        tracker.bind_apple("apple_001", "/apple/1")
        with self.assertRaises(ValueError):
            tracker.bind_apple("apple_001", "/apple/2")
        with self.assertRaises(ValueError):
            tracker.bind_apple("apple_002", "/apple/1")


if __name__ == "__main__":
    unittest.main()
