import ast
from pathlib import Path

import numpy as np
import pytest


PROJECT_DIR = Path(__file__).resolve().parents[1]


def load_cross_section_helper():
    source = (PROJECT_DIR / "apple_pick.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    function = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "_robust_local_cross_section"
    )
    namespace = {"np": np}
    exec(
        compile(ast.Module(body=[function], type_ignores=[]), "apple_pick.py", "exec"),
        namespace,
    )
    return namespace["_robust_local_cross_section"]


cross_section = load_cross_section_helper()


def cylinder_points(radius=0.03, length=0.04, rings=5, samples=48):
    result = []
    for z_value in np.linspace(-0.5 * length, 0.5 * length, rings):
        for angle in np.linspace(0.0, 2.0 * np.pi, samples, endpoint=False):
            result.append(
                [radius * np.cos(angle), radius * np.sin(angle), z_value]
            )
    return np.asarray(result, dtype=float)


def test_straight_branch_keeps_authored_radius():
    center, radius = cross_section(cylinder_points(), np.array([0.0, 0.0, 1.0]))

    np.testing.assert_allclose(center, np.zeros(3), atol=1e-9)
    assert radius == pytest.approx(0.03, abs=1e-6)


def test_one_sided_fork_does_not_inflate_main_branch_capsule():
    trunk = cylinder_points()
    fork = np.column_stack(
        (
            np.linspace(0.05, 0.25, 36),
            np.zeros(36),
            np.linspace(-0.015, 0.015, 36),
        )
    )

    _center, radius = cross_section(
        np.vstack((trunk, fork)), np.array([0.0, 0.0, 1.0])
    )

    # 한쪽 fork 점 때문에 소폭 보수적으로 커지는 것은 허용하되, 기존 RMS처럼
    # fork 길이를 capsule 반경으로 흡수해서는 안 된다.
    assert radius == pytest.approx(0.03, abs=0.004)
    assert radius < 0.05


def test_rotated_branch_uses_local_axis_not_world_axis():
    points = cylinder_points()
    rotation = np.array(
        [
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
        ]
    )
    rotated = points @ rotation.T + np.array([0.4, -0.2, 1.1])

    center, radius = cross_section(rotated, rotation @ np.array([0.0, 0.0, 1.0]))

    np.testing.assert_allclose(center, [0.4, -0.2, 1.1], atol=1e-9)
    assert radius == pytest.approx(0.03, abs=1e-6)


def test_harvest_branchbody_is_excluded_from_physx_and_planning_collision():
    source = (PROJECT_DIR / "apple_pick.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    collect_function = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "_collect_tree_planning_geometry"
    )
    collect_source = ast.get_source_segment(source, collect_function)

    assert "disable_branchbody_collisions(stage)" in source
    assert "collision.CreateCollisionEnabledAttr(False).Set(False)" in source
    assert "for root_path in (TREE_ROOT_PATH,):" in collect_source
    assert "*BRANCH_BODY_PATHS" not in collect_source


def test_empty_tree_proxy_set_has_infinite_clearance_instead_of_min_error():
    source = (PROJECT_DIR / "apple_pick.py").read_text(encoding="utf-8")

    assert 'return float("inf"), "no_planning_proxy"' in source
    assert 'return float("inf"), "no_tree_proxy"' in source


def test_unified_component_160_is_excluded_from_physx_and_planning():
    source = (PROJECT_DIR / "apple_pick.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    functions = {
        node.name: ast.get_source_segment(source, node)
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name in {
            "configure_unified_tree_physx_colliders",
            "_collect_tree_planning_geometry",
        }
    }

    assert "EXCLUDED_UNIFIED_TREE_COMPONENT_INDICES = frozenset({160})" in source
    assert "component_index in EXCLUDED_UNIFIED_TREE_COMPONENT_INDICES" in functions[
        "configure_unified_tree_physx_colliders"
    ]
    assert "component_index in EXCLUDED_UNIFIED_TREE_COMPONENT_INDICES" in functions[
        "_collect_tree_planning_geometry"
    ]
