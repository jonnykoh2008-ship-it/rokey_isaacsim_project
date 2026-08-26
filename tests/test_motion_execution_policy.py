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


def load_rrt_iteration_policy():
    source = (PROJECT_DIR / "apple_pick.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    wanted = {
        "RRT_DEFAULT_MAX_ITERATIONS",
        "RRT_FAST_TRANSFER_MAX_ITERATIONS",
        "RRT_FAST_TRANSFER_STATES",
    }
    nodes = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            names = {
                target.id
                for target in node.targets
                if isinstance(target, ast.Name)
            }
            if names & wanted:
                nodes.append(node)
        elif (
            isinstance(node, ast.FunctionDef)
            and node.name == "rrt_max_iterations_for_segment"
        ):
            nodes.append(node)
    namespace = {}
    exec(
        compile(ast.Module(body=nodes, type_ignores=[]), "apple_pick.py", "exec"),
        namespace,
    )
    return namespace


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


def test_post_tree_transfer_uses_bounded_cpu_rrt_iterations():
    policy = load_rrt_iteration_policy()
    limit_for = policy["rrt_max_iterations_for_segment"]
    fast_limit = policy["RRT_FAST_TRANSFER_MAX_ITERATIONS"]
    default_limit = policy["RRT_DEFAULT_MAX_ITERATIONS"]

    assert fast_limit == 3000
    assert fast_limit < default_limit
    assert limit_for("NEUTRAL_TRANSFER") == fast_limit
    assert limit_for("ALIGN_HALF") == fast_limit
    assert limit_for("TREE_EXIT") == default_limit


def test_fast_transfer_converts_task_target_to_warm_start_cspace_goal():
    source = (PROJECT_DIR / "apple_pick.py").read_text(encoding="utf-8")

    assert "segment_name in RRT_FAST_TRANSFER_STATES" in source
    assert "warm_start=active_positions" in source
    assert "[RRT IK GOAL]" in source
