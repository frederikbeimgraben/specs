# CLAUDE.md

This repository is a starter kit for specs. `README.md` tells what it does.

- `specs/conventions/specs/` and `specs/workflow/specs/` hold the base rules. They are specs, and they win over this file (000001).
- `specs/agents/` holds the rules for agents. Read them before each task.
- `specs/style/` holds the code style. The Python code in `src/` follows it.
- A change of a rule starts as a spec change with `status: draft` (000002). The owner approves it.
- All text follows ASD-STE100 (000025).
- Skills: `spec-write`, `spec-structure`, `spec-approve`, `spec-check`, `spec-adopt`.
- Command: `nix run . -- <command>`. Check: `nix run . -- check --write`. It must show 0 errors.
- Code check: `nix develop -c ruff check src`, `nix develop -c basedpyright`. Both must show 0 errors.
- `specs init` and `specs update` copy `.specs/templates/`, the skills `.claude/skills/spec-*` and `src/specs_kit/data/` into a project. A new file of the kit that a project needs must be in one of these places.
