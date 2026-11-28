---
id: "000084"
title: spezi.toml switches the optional parts of the kit on and off
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/project.py
  - src/spezi/install.py
  - src/spezi/kit.py
  - src/spezi/devshell.py
  - src/spezi/check.py
  - src/spezi/data/spezi.toml
scope:
  - src/spezi/
  - spezi.toml
---

# spezi.toml switches the optional parts of the kit on and off

The table `[features]` of `spezi.toml` must hold one switch, `true` or `false`, for each
optional part of the kit. A missing switch is `true`.

| Switch | Part of the kit | Removal when the switch is `false` |
| --- | --- | --- |
| `mcp` | The entry `spezi` in `.mcp.json` (spec 000066). | Remove the entry. Remove `.mcp.json` when nothing stays. |
| `agents` | The block in `AGENTS.md` (spec 000079). | Remove the block. Remove `AGENTS.md` when nothing stays. |
| `claude` | `CLAUDE.md` with the line `@AGENTS.md` (spec 000079). | Remove the file when it holds only this line, else show the line to remove. |
| `ci` | The CI job (spec 000066) and the entry in `.gitlab-ci.yml`. | Remove the CI file and the entry. |
| `skills` | The skills `.claude/skills/spezi-*`. | Remove the folders. |
| `flake` | `flake.nix` and `flake.lock` with the devShell (spec 000066). | Remove both when `flake.nix` holds only the text of the kit, else show what to remove. |
| `envrc` | `.envrc` with `use flake`. | Remove the file when it holds only `use flake`, else show the line to remove. |

Reason: A project takes only the parts of the kit that it uses, and one place tells which parts
these are.

Test: `tests/test_features.py`.
