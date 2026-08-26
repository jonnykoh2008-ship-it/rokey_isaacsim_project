import ast
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]


def assigned_string_set(path, variable_name):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(
            isinstance(target, ast.Name) and target.id == variable_name
            for target in node.targets
        ):
            continue
        return {
            item.value
            for item in node.value.elts
            if isinstance(item, ast.Constant) and isinstance(item.value, str)
        }
    raise AssertionError(f"{variable_name} assignment not found")


def test_conveyor_alignment_states_use_rrt_trajectory_execution():
    states = assigned_string_set(
        PROJECT_DIR / "vision_apple_pick.py",
        "RRT_FSM_STATES",
    )

    assert {"ALIGN_HALF", "ALIGN_DOWN"} <= states


def test_robot_and_tree_collider_visuals_are_opt_in():
    source = (PROJECT_DIR / "apple_pick.py").read_text(encoding="utf-8")

    assert '"--show-colliders"' in source
    assert "if args.show_colliders" in source
    assert "if not args.show_colliders:" in source
