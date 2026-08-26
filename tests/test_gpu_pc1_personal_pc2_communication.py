import ast
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from appleproj_interfaces.msg import SimulationState

from conveyor_checkpoint_tracker import (
    INSPECTION_CHECKPOINT_ID,
    ConveyorBounds,
    InspectionCheckpointTracker,
)


PROJECT_DIR = Path(__file__).resolve().parents[1]


def load_retry_evaluator():
    """Load the pure helper without starting vision_apple_pick's SimulationApp."""
    source = (PROJECT_DIR / "vision_apple_pick.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    function = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "evaluate_retry_inspection_request"
    )
    namespace = {}
    exec(
        compile(
            ast.Module(body=[function], type_ignores=[]),
            filename="vision_apple_pick.py",
            mode="exec",
        ),
        namespace,
    )
    return namespace["evaluate_retry_inspection_request"]


def load_retry_callback(evaluator):
    source = (PROJECT_DIR / "vision_apple_pick.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    robot_node = next(
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == "RobotMotionNode"
    )
    method = next(
        node
        for node in robot_node.body
        if isinstance(node, ast.FunctionDef) and node.name == "retry_inspection"
    )
    namespace = {
        "SimulationState": SimulationState,
        "evaluate_retry_inspection_request": evaluator,
    }
    exec(
        compile(
            ast.Module(body=[method], type_ignores=[]),
            filename="vision_apple_pick.py",
            mode="exec",
        ),
        namespace,
    )
    return namespace["retry_inspection"]


class GpuPc1PersonalPc2CommunicationTest(unittest.TestCase):
    def setUp(self):
        self.evaluate_retry = load_retry_evaluator()

    def test_retry_rejects_empty_required_fields(self):
        accepted, new_id, message = self.evaluate_retry("", "apple_001", "blur", True)

        self.assertFalse(accepted)
        self.assertEqual("", new_id)
        self.assertIn("inspection_id", message)

    def test_retry_rejects_when_simulation_is_not_ready(self):
        accepted, new_id, message = self.evaluate_retry(
            "inspection_001", "apple_001", "blur", False
        )

        self.assertFalse(accepted)
        self.assertEqual("", new_id)
        self.assertIn("READY", message)

    def test_retry_reports_missing_gpu_pc2_handoff_without_false_acceptance(self):
        accepted, new_id, message = self.evaluate_retry(
            "inspection_001", "apple_001", "blur", True
        )

        self.assertFalse(accepted)
        self.assertEqual("", new_id)
        self.assertIn("GPU PC 2", message)

    def test_retry_service_callback_populates_rejection_response(self):
        callback = load_retry_callback(self.evaluate_retry)
        logger = SimpleNamespace(warning=lambda _message: None)
        node = SimpleNamespace(
            lock=threading.Lock(),
            simulation_state=SimulationState.PLAYING,
            get_logger=lambda: logger,
        )
        request = SimpleNamespace(
            inspection_id="inspection_001",
            apple_id="apple_001",
            reason="blur",
        )
        response = SimpleNamespace(
            accepted=True,
            new_inspection_id="should-be-cleared",
            message="",
        )

        returned = callback(node, request, response)

        self.assertIs(response, returned)
        self.assertFalse(response.accepted)
        self.assertEqual("", response.new_inspection_id)
        self.assertIn("GPU PC 2", response.message)

    def test_checkpoint_tracker_emits_exact_enter_exit_edges(self):
        bounds = ConveyorBounds(
            minimum=np.array([0.0, -0.5, 0.0]),
            maximum=np.array([2.0, 0.5, 0.2]),
            travel_axis=0,
        )
        records = []
        tracker = InspectionCheckpointTracker(bounds, (0.25, 0.75), records.append)
        tracker.bind_apple("apple_001", "/World/apple_001")

        tracker.update({"/World/apple_001": np.array([0.2, 0.0, 0.1])})
        tracker.update({"/World/apple_001": np.array([0.6, 0.0, 0.1])})
        tracker.update({"/World/apple_001": np.array([0.7, 0.0, 0.1])})
        tracker.update({"/World/apple_001": np.array([1.8, 0.0, 0.1])})

        self.assertEqual(2, len(records))
        self.assertEqual(INSPECTION_CHECKPOINT_ID, records[0].checkpoint_id)
        self.assertTrue(records[0].entered)
        self.assertFalse(records[1].entered)


if __name__ == "__main__":
    unittest.main()
