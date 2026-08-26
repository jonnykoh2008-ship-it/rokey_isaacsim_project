import ast
from pathlib import Path

import numpy as np
import pytest


PROJECT_DIR = Path(__file__).resolve().parents[1]


def load_geometry_helpers():
    source = (PROJECT_DIR / "apple_pick.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    wanted_constants = {
        "CONVEYOR_END_INSET_M",
        "CONVEYOR_OUTSIDE_OFFSET_M",
        "CONVEYOR_EDGE_CLEARANCE_M",
    }
    nodes = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            names = {target.id for target in node.targets if isinstance(target, ast.Name)}
            if names & wanted_constants:
                nodes.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name in {
            "compute_conveyor_target_geometry",
            "compute_direct_neutral_transfer",
            "select_conveyor_surface_layer",
        }:
            nodes.append(node)
    namespace = {"np": np}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), "apple_pick.py", "exec"), namespace)
    return (
        namespace["compute_conveyor_target_geometry"],
        namespace["compute_direct_neutral_transfer"],
        namespace["select_conveyor_surface_layer"],
    )


compute_geometry, compute_neutral_transfer, select_surface_layer = (
    load_geometry_helpers()
)


class FakeBox:
    def __init__(self, minimum, maximum):
        self.minimum = np.asarray(minimum, dtype=float)
        self.maximum = np.asarray(maximum, dtype=float)

    def GetMin(self):
        return self.minimum

    def GetMax(self):
        return self.maximum


def surface_candidate(score, minimum, maximum):
    box = FakeBox(minimum, maximum)
    size = box.maximum - box.minimum
    return score, object(), box, size


def test_wider_belt_uses_nearest_valid_edge_instead_of_center_band():
    start, outside, _direction, travel_axis, side_axis, side_inset = compute_geometry(
        np.array([-0.75, -0.40, 0.50]),
        np.array([0.75, 0.40, 0.56]),
        np.array([0.0, 1.20, 0.0]),
        np.array([0.08, 0.08, 0.08]),
    )

    assert travel_axis == 0
    assert side_axis == 1
    assert side_inset == pytest.approx(0.07)
    assert start[1] == pytest.approx(0.33)
    assert outside[1] == pytest.approx(0.70)


def test_place_center_keeps_whole_apple_inside_changed_width():
    minimum = np.array([-0.75, -0.18, 0.50])
    maximum = np.array([0.75, 0.18, 0.56])
    apple_size = np.array([0.08, 0.10, 0.08])
    start, _outside, _direction, _travel_axis, side_axis, side_inset = compute_geometry(
        minimum, maximum, np.array([0.0, -1.0, 0.0]), apple_size
    )

    assert start[side_axis] == pytest.approx(minimum[side_axis] + side_inset)
    assert start[side_axis] - 0.5 * apple_size[side_axis] >= minimum[side_axis] + 0.03


def test_rejects_belt_narrower_than_apple_and_edge_clearance():
    with pytest.raises(RuntimeError, match="유효 폭"):
        compute_geometry(
            np.array([-0.75, -0.06, 0.50]),
            np.array([0.75, 0.06, 0.56]),
            np.array([0.0, 1.0, 0.0]),
            np.array([0.08, 0.08, 0.08]),
        )


def test_tree_clear_pose_bypasses_fixed_exit_offset():
    retreat = np.array([0.9885, 0.4702, 1.0200])
    conveyor_outside_high = np.array([1.20, -0.40, 1.3558])

    neutral = compute_neutral_transfer(retreat, conveyor_outside_high)

    np.testing.assert_allclose(neutral[:2], [1.09425, 0.0351])
    assert neutral[2] == pytest.approx(1.3558)
    assert np.linalg.norm(neutral[:2] - retreat[:2]) < 0.45


def test_surface_layer_keeps_changed_width_without_using_high_frame_plane():
    left_surface = surface_candidate(
        100.0,
        [-0.75, -0.40, 0.50],
        [0.75, 0.00, 0.56],
    )
    right_surface = surface_candidate(
        95.0,
        [-0.75, 0.00, 0.50],
        [0.75, 0.40, 0.56],
    )
    high_frame = surface_candidate(
        20.0,
        [-0.90, -0.50, 0.45],
        [0.90, 0.50, 0.92],
    )

    minimum, maximum, layer, anchor, _tolerance = select_surface_layer(
        [left_surface, right_surface, high_frame]
    )

    np.testing.assert_allclose(minimum, [-0.75, -0.40, 0.50])
    np.testing.assert_allclose(maximum, [0.75, 0.40, 0.56])
    assert layer == [left_surface, right_surface]
    assert anchor is left_surface


def test_surface_layer_rejects_empty_candidates():
    with pytest.raises(ValueError, match="비어"):
        select_surface_layer([])
