import ast
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import yaml


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


def load_policy_function(function_name, constants=()):
    source = (PROJECT_DIR / "apple_pick.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    function = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == function_name
    )
    constant_nodes = []
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        names = {
            target.id
            for target in node.targets
            if isinstance(target, ast.Name)
        }
        if names & set(constants):
            constant_nodes.append(node)
    namespace = {"np": np}
    exec(
        compile(
            ast.Module(body=constant_nodes + [function], type_ignores=[]),
            "apple_pick.py",
            "exec",
        ),
        namespace,
    )
    return namespace[function_name]


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
    assert "ik_seeds = [active_positions, central_equivalent, limit_midpoint]" in source
    assert "warm_start=seed" in source
    assert "select_short_periodic_goal(" in source
    assert "[RRT IK GOAL]" in source


def test_positive_physx_contact_separation_is_ignored_as_proximity():
    minimum_separation = load_policy_function(
        "contact_report_minimum_separation"
    )
    header = SimpleNamespace(num_contact_data=2, contact_data_offset=1)
    contact_data = [
        SimpleNamespace(separation=-1.0),
        SimpleNamespace(separation=0.004),
        SimpleNamespace(separation=0.002),
    ]
    source = (PROJECT_DIR / "apple_pick.py").read_text(encoding="utf-8")

    assert minimum_separation(header, contact_data) == 0.002
    assert "minimum_separation > 0.0" in source


def test_actual_gripper_envelope_clearance_uses_tcp_and_both_radii():
    clearance = load_policy_function("gripper_envelope_apple_clearance")

    assert np.isclose(
        clearance(
            tcp_position=[0.0, 0.0, 0.0],
            gripper_radius=0.12,
            apple_center=[0.30, 0.0, 0.0],
            apple_radius=0.06,
        ),
        0.12,
    )


def test_enter_slow_uses_four_millimeter_noncontact_palm_offset():
    source = (PROJECT_DIR / "apple_pick.py").read_text(encoding="utf-8")

    assert "ENTER_CONTACT_EXTENSION_M" not in source
    assert "entry_contact_target" not in source
    assert "(apple_center, approach_rotation, ENTER_SLOW_STEPS" in source
    assert "APPLE_APPROACH_MIN_SURFACE_GAP_M = 0.004" in source
    assert "PALM_CONTACT_CLEARANCE_M = APPLE_APPROACH_MIN_SURFACE_GAP_M" in source


def test_palm_unload_geometry_remains_two_millimeters_but_executor_rejects_contact():
    target_for = load_policy_function(
        "palm_contact_unload_target",
        constants=("PALM_CONTACT_UNLOAD_DISTANCE_M",),
    )
    target = target_for(
        contact_position=[1.0, 2.0, 3.0],
        approach_direction=[0.0, 4.0, 0.0],
    )
    executor_source = (PROJECT_DIR / "vision_apple_pick.py").read_text(
        encoding="utf-8"
    )

    assert np.allclose(target, [1.0, 1.998, 3.0])
    assert "[PALM UNLOAD]" not in executor_source
    assert "GRASP 시작 전에 palm 접촉이 기록되었습니다" in executor_source


def test_enter_slow_allows_grasp_only_from_noncontact_standoff():
    source = (PROJECT_DIR / "vision_apple_pick.py").read_text(encoding="utf-8")

    assert "completion_allowed=True" in source
    assert "[GRASP STANDOFF] ENTER_SLOW 100%" in source
    assert "palm-사과 접촉이 확인되지 않아 GRASP를 허용하지 않습니다." not in source
    assert "compute_gripper_apple_surface_clearance" in source
    assert "complete_current_at_standoff" in source
    assert "[4MM STANDOFF]" in source
    assert "GRASP 전 palm collider가 사과에 직접 접촉했습니다" in source


def test_dynamic_tf_is_robot_prefixed_and_not_published_by_raw_transform_tree():
    source = (PROJECT_DIR / "vision_apple_pick.py").read_text(encoding="utf-8")

    assert "TransformBroadcaster" in source
    assert "child_frame = f\"{robot_id}/" in source
    assert "ROS2PublishTransformTree" not in source


def test_only_staging_rrt_segments_receive_actual_mesh_envelope_check():
    is_staging = load_policy_function("is_staging_rrt_segment")
    source = (PROJECT_DIR / "apple_pick.py").read_text(encoding="utf-8")

    assert is_staging("STAGING direct")
    assert is_staging("STAGING replan +side")
    assert is_staging("STAGING replan -side")
    assert not is_staging("TREE_EXIT")
    assert not is_staging("NEUTRAL_TRANSFER")
    assert "apply_staging_gripper_envelope_check" in source
    assert "[TARGET APPLE REJECT]" in source


def test_lula_description_does_not_add_three_finger_planning_proxies():
    description = yaml.safe_load(
        (PROJECT_DIR / "m0617_robot_description.yaml").read_text(encoding="utf-8")
    )
    gripper_spheres = next(
        item["gripper_frame"]
        for item in description["collision_spheres"]
        if "gripper_frame" in item
    )

    assert len(gripper_spheres) == 2


def test_approach_executes_world_z_before_constructing_fallback_planners():
    source = (PROJECT_DIR / "vision_apple_pick.py").read_text(encoding="utf-8")
    approach = source.split("    def _approach(", 1)[1].split(
        "    def _report_grasp_state", 1
    )[0]

    assert "for candidate_index, candidate in enumerate(candidate_specs):" in approach
    assert "if candidate_index == 0:" in approach
    assert "candidate_motion = preview_motion" in approach
    assert "preflight_candidates.sort" not in approach
    assert "[APPROACH RANK]" not in approach


def test_place_transfer_selects_short_ik_solution_across_joint_four_boundary():
    select_goal = load_policy_function("select_short_periodic_goal")
    current = np.array([0.0, 0.0, 0.0, -6.10, 0.0, 0.0])
    long_boundary_goal = np.array([0.1, 0.2, 0.1, 6.119, 0.2, 0.1])
    short_goal = np.array([0.1, 0.2, 0.1, -5.95, 0.2, 0.1])
    lower = np.full(6, -2.0 * np.pi)
    upper = np.full(6, 2.0 * np.pi)

    selected, selected_index, periodic, periodic_travel = select_goal(
        current,
        [long_boundary_goal, short_goal],
        lower,
        upper,
    )

    assert periodic.all()
    assert selected_index == 1
    np.testing.assert_allclose(selected, short_goal)
    assert periodic_travel < np.pi
