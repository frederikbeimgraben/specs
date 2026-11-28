---
id: "000084"
title: spezi.toml switches the optional parts of the kit on and off
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
tests:
  - tests/test_features.py:test_a_switch_off_removes_the_part
  - tests/test_features.py:test_a_switch_on_writes_the_part_again
  - tests/test_features.py:test_a_changed_claude_file_stays
  - tests/test_features.py:test_claude_needs_agents
  - tests/test_features.py:test_update_follows_the_switches
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
| `mcp` | The entry `spezi` in `.mcp.json` (000066). | Remove the entry. Delete `.mcp.json` when nothing stays. |
| `agents` | The block in `AGENTS.md` (000079). | Remove the block. Delete `AGENTS.md` when nothing stays. |
| `claude` | `CLAUDE.md` with the line `@AGENTS.md` (000079). | Delete the file when it holds only this line, else show the line to remove. |
| `ci` | The CI job of 000066 and the entry in `.gitlab-ci.yml`. | Delete the CI file and remove the entry. |
| `skills` | The skills `.claude/skills/spezi-*`. | Delete the folders. |
| `flake` | `flake.nix` and `flake.lock` with the devShell of 000066. | Delete both when `flake.nix` holds only the text of the kit, else show what to remove. |
| `envrc` | `.envrc` with `use flake`. | Delete the file when it holds only `use flake`, else show the line to remove. |

The index `specs/README.md`, the copies below `specs/.upstream/` and the templates in
`specs/.templates/` have no switch. `spezi init`, `spezi update` and `spezi install` must write
or replace only the parts that are on. `spezi install` must remove each part that is off, as
the table tells, and list each changed or deleted file (000077). `spezi update` must not change
`flake.nix` when `flake` is off. `spezi check` must not check the block in `AGENTS.md` when
`agents` is off.

`claude = true` with `agents = false` is an error of `spezi.toml` (000078), because `CLAUDE.md`
only imports `AGENTS.md`. A key of `[features]` that is not in the table, or a value that is not
`true` or `false`, is also an error of `spezi.toml`.

Reason: A project takes only the parts of the kit that it uses, and one place tells which parts
these are.

Test: `tests/test_features.py`.
