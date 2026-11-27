---
id: "000083"
title: specs install brings a project to the state of its settings
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
tests:
  - tests/test_install.py:test_install_changes_nothing_on_a_current_project
  - tests/test_install.py:test_install_restores_a_changed_copy
  - tests/test_install.py:test_install_writes_missing_kit_files
  - tests/test_install.py:test_install_keeps_a_changed_template
  - tests/test_install.py:test_install_loads_a_missing_copy
implementation:
  - src/specs_kit/install.py
  - src/specs_kit/kit.py
  - src/specs_kit/cli.py
  - src/specs_kit/mcp_server.py
scope:
  - src/specs_kit/
---

# specs install brings a project to the state of its settings

`specs install` must not change a `ref` of `specs.toml` or a commit of `specs.lock` (000082).
It must do these steps in this order:

1. Stop with an error when this program is an older commit of the kit than the kit commit in
   `specs.lock`.
2. Run the migrations that the kit commit of the project does not hold (000081).
3. For each repository of `specs.toml` whose copy does not agree with `specs.lock`, load the
   copy again (000048). When `ref` did not change, it must load the commit of `specs.lock`.
   Else it must resolve `ref` again and write the new commit to `specs.lock`. A copy that a
   person changed agrees no more, so the command loads it again and lists its files as changed
   (000077).
4. Remove each entry of `specs.lock` whose repository is not in `specs.toml`.
5. Write each file of the table of 000066 that does not exist: the templates, the skills, the
   CI file, the entry `specs` in `.mcp.json`, `.envrc` and `CLAUDE.md`, each only when its
   switch in `[features]` is on (000084). A file that exists must not change, also when it is
   not the same as in the kit. Remove each part whose switch is off, as 000084 tells.
6. Write the index `specs/README.md` (000007) and the block in `AGENTS.md` (000079).
7. Run `specs check` (000065) and print its report after its own message. End with the exit
   code 1 when the check finds errors.

When each copy agrees with `specs.lock` and this program is the kit at the commit of
`specs.lock`, the command must not use the network. `specs init`, `specs update` and
`specs add` must end with these steps. The MCP server must have the tool `install`, which does
the same and returns the hints, the report and the changed files (000074).

Reason: One command makes a fresh clone, a changed copy or a missing file current, and writes
each file that the check needs. Only `specs update` and `specs add` change a version, so a
version never changes by accident.

Test: `tests/test_install.py`.
