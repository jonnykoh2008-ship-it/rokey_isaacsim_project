# Repository Working Rules

## Approval gate

- Do not create, modify, rename, move, or delete any file or source code unless the user explicitly approves that specific change.
- Discussion, analysis, planning, review, and read-only inspection do not constitute approval to edit files.
- Before editing, state the intended files and the scope of the change, then wait for explicit approval unless the user has already approved that exact scope.
- Approval applies only to the files and scope named by the user. Ask again before expanding the scope.
- After an approved edit, report the files changed and the verification performed.

## Project baseline

- Target simulator: NVIDIA Isaac Sim 5.1.0 only.
- Target middleware: ROS 2 Jazzy on Ubuntu 24.04 using Fast DDS.
- Use Isaac Sim simulation time through `/clock`; all ROS 2 nodes use `use_sim_time:=true`.
- Preserve the distinction between feature specifications (`docs/features`) and delivery phases (`docs/phases`). Phase documents reference feature documents rather than duplicating them.
- Unresolved requirements must be written as `TBD`; do not invent final values without user approval.

## PC ownership and edit boundaries

This repository is developed by four PCs. Source ownership follows the PC that
executes and maintains the function, not the PC that happens to discover a bug.

| Owner | Responsibilities | Current owned source examples |
|---|---|---|
| GPU PC 1 | Isaac Sim, physics, RGB-D/CameraInfo/TF sensors, planning-scene publication, Lula RRT/trajectory/RMPflow planning and execution, robot Action execution, motion visualization, and runtime safety monitoring | `apple_pick.py`, `vision_apple_pick.py`, `base_camera_publish.py`, `harvest_coordinator.py`, `harvest_route_planner.py` (v2.0 execution ownership), Isaac Sim robot/gripper assets and runtime configuration |
| GPU PC 2 | Quality-image inference and apple-level quality-result integration | Quality inference and result-integration source; current path is `TBD` |
| Personal PC 1 | RGB-D video subscription, apple detection, depth projection, world-coordinate target publication, and remote RViz display | PC1 perception node and RViz configuration; current path is `TBD` |
| Personal PC 2 | Monitoring, result display, retry requests, and phase-2 pusher selection | Monitoring and pusher-selection source; current path is `TBD` |

v2.0 경계를 쉽게 표현하면 개인 PC 1은 영상을 보는 눈, GPU PC 1은 경로를 결정하고
로봇을 움직이는 두뇌와 팔, 개인 PC 1의 RViz는 계획을 보여 주는 화면이다. Lula RRT는
transit/staging/pre-grasp/retract의 큰 이동길에 사용하고, grasp/twist/pull은 접촉을
보장하는 정밀 동작으로 유지한다.

Shared contracts and documentation include `appleproj_interfaces/`, `docs/`,
`README.md`, `AGENTS.md`, and cross-PC build or network configuration. They are
not owned exclusively by one PC. Modify a shared file only after the user
explicitly approves that exact file and scope, and report every affected PC.

The active implementation scope is task-specific and must be established from
the user's request and the execution PC. This document does not designate one
PC as the permanent current work environment.

- Before every source edit, state which PC executes the code and confirm that
  the file belongs to that PC. If ownership is missing or ambiguous, stop and
  ask the user instead of editing.
- Do not make opportunistic edits to another PC's source while changing shared
  interfaces or documentation.
- A request to fix system behavior does not by itself transfer ownership of the
  executing PC's source. If the fix belongs to another PC, identify that owner
  and obtain the required approval for the file and scope.
- When a change is needed in another PC's source, submit a modification review
  request to that PC's owner instead of editing the file. Include the target
  file and function, observed problem, proposed behavior, interface impact,
  and verification steps.

## Required documentation routing

Before planning or implementing a task, read the documents mapped to its scope.

| Task scope | Required documents |
|---|---|
| Project-wide architecture | `README.md`, `docs/architecture/system_overview.md` |
| Apple or obstacle perception | `docs/features/harvest_perception.md`, `docs/architecture/tf_frames.md`, `docs/architecture/ros2_interfaces.md` |
| Robot motion, grasping, or Twist & Pull | `docs/features/harvesting.md`, `docs/assets/asset_requirements.md`, `docs/architecture/tf_frames.md` |
| MVP implementation | `docs/phases/phase_1_mvp.md` plus all relevant feature documents |
| Conveyor implementation | `docs/features/conveyor.md`, `docs/assets/asset_requirements.md`, `docs/architecture/ros2_interfaces.md` |
| Quality inspection or grading | `docs/features/quality_grading.md`, `docs/features/conveyor.md`, `docs/architecture/ros2_interfaces.md` |
| Domain randomization or AI training | `docs/phases/phase_2_ai_randomization.md` plus the relevant perception or grading documents |
| Physical pusher implementation | `docs/phases/phase_2_pusher.md`, `docs/features/conveyor.md`, `docs/features/quality_grading.md`, `docs/architecture/ros2_interfaces.md` |
| Rail or multi-tree integration | `docs/phases/phase_3_system_integration.md`, `docs/architecture/system_overview.md`, and all affected feature documents |
| ROS 2 topics, messages, or QoS | `docs/architecture/ros2_interfaces.md`, `docs/architecture/tf_frames.md` |
| Multi-PC or network setup | `docs/architecture/hardware_network.md`, `docs/architecture/ros2_interfaces.md` |
| Robot, gripper, camera, apple, tree, or conveyor assets | `docs/assets/asset_requirements.md` plus the relevant feature document |
| TF, frame, timestamp, or simulation-time work | `docs/architecture/tf_frames.md`, `docs/architecture/ros2_interfaces.md` |

### Routing rules

- Read all required documents completely before planning or modifying code.
- For a phase-specific task, read both the phase document and every affected feature document.
- Feature documents define how a function behaves; phase documents define when and how much of it is implemented.
- Architecture documents take precedence over duplicated interface, TF, timing, or network descriptions in feature documents.
- Instructions in the user's current request take precedence over repository documentation only within the explicitly approved scope.
- If documents conflict, do not choose one silently. Report the conflict and request a decision.
- Do not implement `TBD` requirements by inventing permanent values. Temporary values require explicit user approval.
- Before editing, state which documents were used and which files are authorized to change.

## Command interpretation

- Requests to review, analyze, explain, inspect, or plan are read-only and do not authorize file changes.
- Requests to implement, write, create, update, or fix require explicit approval for the files and scope to be changed.
- An approval applies only to the files and scope identified by the user or in the immediately preceding approval request.
- If an approval's target or scope is ambiguous, do not change files; ask the user to clarify the authorized scope.
