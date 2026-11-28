---
id: "000066"
title: spezi init adds the kit to a project
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_kit.py:test_init_writes_the_kit_files
implementation:
  - src/spezi/kit.py
  - src/spezi/devshell.py
  - src/spezi/cli.py
  - src/spezi/install.py
  - src/spezi/data/
scope:
  - src/spezi/
---

# spezi init adds the kit to a project

`spezi init [<dir>] [--forge github|gitlab|codeberg] [-y] [-r]` must add the kit to the project
in `<dir>`, or in the current folder. It must write the answers to the questions (spec 000085) to
`spezi.toml`. It must write these files:

| File | Content |
| --- | --- |
| `spezi.toml` | The settings, with the answers (spec 000085) and the `ref` of the kit that `spezi add` proposes (spec 000303). |
| `spezi.lock` | The commit that this `ref` names, the hash of the copy of the kit, and the entry of each copy of a transitive upstream (spec 000082). |
| `specs/` | An empty folder for the rules of the project. |
| `specs/.upstream/github.com/frederikbeimgraben/spezi/` | The rules of the kit at this commit, with its `spezi.lock` (spec 000048). |
| `specs/.upstream/<repo>/` | The transitive upstreams of the kit that the user chooses, or each with `-r` (spec 000092, 000085). The command writes them as `transitive` to the table of the kit. |
| `specs/.templates/` | The templates of the kit at this commit. |
| `.claude/skills/spezi-*` | The skills of the kit. |
| `.github/workflows/spezi.yml`, `.gitlab/ci/spezi.yml` or `.forgejo/workflows/spezi.yml` | The CI job for the forge (spec 000283). |
| `.gitlab-ci.yml` | Only for GitLab: the entry `- local: .gitlab/ci/spezi.yml` below `include:`, if it is not there. The other content stays. |
| `.mcp.json` | The MCP server `spezi` at the commit of the kit. Other servers stay. |

Reason: One command gives a project the same start as every other project.

Test: `tests/test_kit.py`.
