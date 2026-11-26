# CLAUDE.md

This repository is a starter kit for specs. `README.md` tells what it does.

- `specs/conventions/specs/` and `specs/workflow/specs/` hold the base rules. They are specs, and they win over this file (000001).
- `specs/agents/` holds the rules for agents. Read them before each task.
- A change of a rule starts as a spec change with `status: draft` (000002). The owner approves it.
- All text follows ASD-STE100 (000025).
- Skills: `spec-write`, `spec-structure`, `spec-approve`, `spec-check`, `spec-adopt`.
- Check: `python3 scripts/check_specs.py --write`. It must show 0 errors.
- `install.sh` copies the kit. A new file of the kit that a project needs must be in its list.
