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