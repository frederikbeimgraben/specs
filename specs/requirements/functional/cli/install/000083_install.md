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
  - tests/test_install.py:test_install_adds_the_line_to_gitattributes
  - tests/test_transitive.py:test_add_with_recursive_copies_the_transitive_upstream
implementation:
  - src/spezi/install.py
  - src/spezi/kit.py
  - src/spezi/cli.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# spezi install brings a project to the state of its settings

`spezi install` must not change a `ref` of `spezi.toml`. It must write a commit to `spezi.lock`
only in step 3 and step 4. It must do these steps in this order:

1. Stop for an older program (spec 000293).
2. Run the migrations that the kit commit of the project does not hold (spec 000081).
3. For each repository of `spezi.toml` whose copy does not agree with `spezi.lock`, load the
   copy again (spec 000048). When `ref` did not change, load the commit of `spezi.lock`. Else
   resolve `ref` again and write the new commit to `spezi.lock`. A copy that a person changed
   agrees no more, so the command loads it again and lists its files (spec 000077).
4. Find each repository of a list `transitive` whose copy does not agree with `spezi.lock`.
   Load its copy again at the commit that the `spezi.lock` in the copy of its direct upstream
   names (spec 000092). Write this commit to `spezi.lock`. Remove each copy and each entry of
   `spezi.lock` whose repository is not in `spezi.toml` and not in a list `transitive`.
5. When `specs/.upstream/` holds a copy, add the line `specs/.upstream/** -text` to
   `.gitattributes` when the file does not hold it (spec 000048).
6. Write each file of the table (spec 000066) that does not exist and whose switch is on
   (spec 000084). These files are the templates, the skills, the CI file, the entry `spezi` in
   `.mcp.json`, `.envrc` and `CLAUDE.md`. A file that exists stays, also when it is not the same
   as in the kit. Remove each part whose switch is off (spec 000084).
7. Write the index `specs/README.md` (spec 000007) and the block in `AGENTS.md` (spec 000079).
8. Run `spezi check` (spec 000065). Print the message of the command, the hints, the changed
   files (spec 000077) and then the report of the check. End with the exit code 1 when the check
   finds errors.

Reason: One command makes a fresh clone, a changed copy or a missing file current, and writes
each file that the check needs. Only `spezi update` and `spezi add` change a `ref`, so a
version never changes by accident.

Test: `tests/test_install.py`.
