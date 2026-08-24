import unittest

import numpy as np

from harvest_route_planner import (
    Proxy,
    RoutePlanningError,
    SHAPE_BOX,
    SHAPE_SPHERE,
    plan_approach_route,
    route_clearance,
    validate_scene_version,
)


IDENTITY = np.array([0.0, 0.0, 0.0, 1.0])
START_ORIENTATION = np.array([0.0, 0.0, np.sqrt(0.5), np.sqrt(0.5)])


class HarvestRoutePlannerTest(unittest.TestCase):
    def test_direct_route(self):
        obstacle = Proxy(
            "far",
            SHAPE_SPHERE,
            np.array([5.0, 5.0, 5.0]),
            IDENTITY,
            np.array([0.1, 0.0, 0.0]),
            0.02,
        )
        route = plan_approach_route(
            np.array([1.5, 0.6, 2.0]),
            np.array([1.5, 0.6, 0.5]),
            np.array([0.8, 0.4, 1.2]),
            [obstacle],
            start_orientation_xyzw=START_ORIENTATION,
        )
        self.assertEqual(route.name, "direct")
        np.testing.assert_allclose(route.positions[-1], [0.8, 0.4, 1.05])
        self.assertEqual(
            [waypoint.phase for waypoint in route.waypoints],
            ["SAFE_TRANSIT", "ORIENTATION_ALIGN", "PRE_GRASP"],
        )
        np.testing.assert_allclose(
            route.waypoints[0].position,
            route.waypoints[1].position,
        )
        np.testing.assert_allclose(
            route.waypoints[0].orientation_xyzw,
            START_ORIENTATION,
        )
        self.assertFalse(
            np.allclose(
                route.waypoints[1].orientation_xyzw,
                START_ORIENTATION,
            )
        )
        np.testing.assert_allclose(
            route.waypoints[1].orientation_xyzw,
            route.waypoints[2].orientation_xyzw,
        )

    def test_outside_route_when_direct_is_blocked(self):
        trunk = Proxy(
            "trunk",
            SHAPE_BOX,
            np.array([1.15, 0.5, 1.3]),
            IDENTITY,
            np.array([0.20, 0.20, 1.20]),
            0.05,
        )
        route = plan_approach_route(
            np.array([1.5, 0.5, 2.0]),
            np.array([1.5, 0.5, 0.5]),
            np.array([0.8, 0.5, 1.2]),
            [trunk],
            start_orientation_xyzw=START_ORIENTATION,
        )
        self.assertTrue(route.name.startswith("outside"))
        self.assertGreaterEqual(route.minimum_clearance, 0.0)
        self.assertEqual(route.waypoints[0].phase, "SAFE_TRANSIT")
        self.assertEqual(route.waypoints[1].phase, "ORIENTATION_ALIGN")
        np.testing.assert_allclose(
            route.waypoints[0].position,
            route.waypoints[1].position,
        )
        np.testing.assert_allclose(
            route.waypoints[0].orientation_xyzw,
            START_ORIENTATION,
        )

    def test_route_clearance_reports_collision(self):
        obstacle = Proxy(
            "sphere",
            SHAPE_SPHERE,
            np.zeros(3),
            IDENTITY,
            np.array([0.2, 0.0, 0.0]),
            0.05,
        )
        clearance, name = route_clearance(
            [np.array([-1.0, 0.0, 0.0]), np.array([1.0, 0.0, 0.0])],
            [obstacle],
        )
        self.assertLess(clearance, 0.0)
        self.assertEqual(name, "sphere")

    def test_invalid_start_is_rejected(self):
        with self.assertRaises(RoutePlanningError):
            plan_approach_route(
                np.array([np.nan, 0.0, 0.0]),
                np.zeros(3),
                np.ones(3),
                [],
                start_orientation_xyzw=IDENTITY,
            )

    def test_invalid_start_orientation_is_rejected(self):
        with self.assertRaises(RoutePlanningError):
            plan_approach_route(
                np.array([1.5, 0.6, 2.0]),
                np.array([1.5, 0.6, 0.5]),
                np.array([0.8, 0.4, 1.2]),
                [],
                start_orientation_xyzw=np.zeros(4),
            )

    def test_no_route_is_rejected(self):
        enclosing = Proxy(
            "enclosing",
            SHAPE_BOX,
            np.array([0.8, 0.4, 1.2]),
            IDENTITY,
            np.array([20.0, 20.0, 20.0]),
            0.05,
        )
        with self.assertRaises(RoutePlanningError):
            plan_approach_route(
                np.array([1.5, 0.6, 2.0]),
                np.array([1.5, 0.6, 0.5]),
                np.array([0.8, 0.4, 1.2]),
                [enclosing],
                start_orientation_xyzw=IDENTITY,
            )

    def test_stale_scene_is_rejected(self):
        with self.assertRaises(RoutePlanningError):
            validate_scene_version(1, 4, 2, 5)
        validate_scene_version(2, 5, 2, 5)


if __name__ == "__main__":
    unittest.main()
