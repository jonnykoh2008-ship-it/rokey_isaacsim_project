import unittest
from pathlib import Path

import yaml


PROJECT_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_DIR / "m0617_rrt_config.yaml"


class M0617RrtConfigTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with CONFIG_PATH.open("r", encoding="utf-8") as stream:
            cls.config = yaml.safe_load(stream)

    def test_required_planner_parameters_are_present(self):
        required = {
            "seed",
            "step_size",
            "max_iterations",
            "max_sampling",
            "distance_metric_weights",
            "task_space_frame_name",
            "task_space_limits",
            "c_space_planning_params",
            "task_space_planning_params",
        }

        self.assertEqual(required - self.config.keys(), set())

    def test_m0617_joint_metric_matches_six_dof_cspace(self):
        weights = self.config["distance_metric_weights"]

        self.assertEqual(len(weights), 6)
        self.assertTrue(all(float(value) > 0.0 for value in weights))

    def test_link6_and_task_space_limits_are_valid(self):
        self.assertEqual(self.config["task_space_frame_name"], "link_6")
        limits = self.config["task_space_limits"]

        self.assertEqual(len(limits), 3)
        self.assertTrue(
            all(
                len(axis) == 2 and float(axis[0]) < float(axis[1])
                for axis in limits
            )
        )

    def test_trial_search_parameters_are_positive(self):
        self.assertGreater(int(self.config["seed"]), 0)
        self.assertGreater(float(self.config["step_size"]), 0.0)
        self.assertGreater(int(self.config["max_iterations"]), 0)
        self.assertGreater(int(self.config["max_sampling"]), 0)

    def test_task_space_sampling_fractions_are_consistent(self):
        parameters = self.config["task_space_planning_params"]
        exploitation = float(parameters["task_space_exploitation_fraction"])
        exploration = float(parameters["task_space_exploration_fraction"])

        self.assertGreaterEqual(exploitation, 0.0)
        self.assertGreaterEqual(exploration, 0.0)
        self.assertLessEqual(exploitation + exploration, 1.0)


if __name__ == "__main__":
    unittest.main()
