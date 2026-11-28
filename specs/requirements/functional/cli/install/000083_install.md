---
id: "000083"
title: spezi install brings a project to the state of its settings
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_install.py:test_install_changes_nothing_on_a_current_project
  - tests/test_install.py:test_install_restores_a_changed_copy
  - tests/test_install.py:test_install_writes_missing_kit_files
  - tests/test_install.py:test_install_keeps_a_changed_template
  - tests/test_install.py:test_install_loads_a_missing_copy
  - tests/test_install.py:test_install_stops_for_a_broken_mcp_file
  - tests/test_install.py:test_install_stops_for_mcp_servers_that_are_no_object
implementation:
  - src/spezi/install.py
  - src/spezi/kit.py
  - src/spezi/cli.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# spezi install brings a project to the state of its settings

`spezi install` must not change a `ref` of `spezi.toml` or a commit of `spezi.lock` (000082).
It must do these steps in this order:

1. Stop with an error when this program is an older commit of the kit than the kit commit in
   `spezi.lock`.
2. Run the migrations that the kit commit of the project does not hold (000081).
3. For each repository of `spezi.toml` whose copy does not agree with `spezi.lock`, load the
   copy again (000048). When `ref` did not change, it must load the commit of `spezi.lock`.
   Else it must resolve `ref` again and write the new commit to `spezi.lock`. A copy that a
   person changed agrees no more, so the command loads it again and lists its files as changed
   (000077).
4. Remove each entry of `spezi.lock` whose repository is not in `spezi.toml`.
5. Write each file of the table of 000066 that does not exist: the templates, the skills, the
   CI file, the entry `spezi` in `.mcp.json`, `.envrc` and `CLAUDE.md`, each only when its
   switch in `[features]` is on (000084). A file that exists must not change, also when it is
   not the same as in the kit. Remove each part whose switch is off, as 000084 tells.
6. Write the index `specs/README.md` (000007) and the block in `AGENTS.md` (000079).
7. Run `spezi check` (000065). Print its own message, the hints, the changed files (000077)
   and then the report of the check. End with the exit code 1 when the check finds errors.

When `.mcp.json` is no valid JSON, is not a JSON object, or has a `mcpServers` that is not an
object, the command must stop with an error that names `.mcp.json`, and must not change
`.mcp.json`.

When each copy agrees with `spezi.lock` and this program is the kit at the commit of
`spezi.lock`, the command must not use the network. `spezi init`, `spezi update` and
`spezi add` must end with these steps. The MCP server must have the tool `install`, which does
the same and returns the hints, the changed files and the report (000074).

Reason: One command makes a fresh clone, a changed copy or a missing file current, and writes
each file that the check needs. Only `spezi update` and `spezi add` change a version, so a
version never changes by accident.

Test: `tests/test_install.py`.
