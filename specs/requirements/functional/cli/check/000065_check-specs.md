---
id: "000065"
title: spezi check checks the specs
kind: functional
status: draft
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_check.py:test_check_passes_after_init
  - tests/test_check.py:test_check_changes_no_file
  - tests/test_check.py:test_install_writes_the_index
  - tests/test_check.py:test_check_finds_a_rule_without_must
  - tests/test_check.py:test_check_finds_a_bad_file_name
  - tests/test_check.py:test_check_finds_a_missing_key
  - tests/test_check.py:test_check_finds_a_stale_index
  - tests/test_check.py:test_check_gives_the_line
  - tests/test_check.py:test_check_finds_a_file_outside_the_kind_folders
  - tests/test_check.py:test_check_gives_the_line_of_the_key
  - tests/test_check.py:test_check_finds_an_old_diagram_type
  - tests/test_check.py:test_check_finds_a_reference_to_no_rule
  - tests/test_check.py:test_check_finds_a_reference_to_a_removed_rule
  - tests/test_check.py:test_check_finds_front_matter_that_is_no_yaml
  - tests/test_check.py:test_check_finds_a_rule_of_a_copy_that_it_cannot_read
implementation:
  - src/spezi/agents.py
  - src/spezi/check.py
  - src/spezi/index.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# spezi check checks the specs

`spezi check` must run every check of the conventions on the specs of the project. It must also
check that `spezi.toml`, `spezi.lock` and the copies of 000048 agree (000082), and check each
`§` reference in `code_dirs` (000017). It must read each rule of the copies, report each rule
that it cannot read, for example without front matter, and not count it. It must not run the
other checks of the conventions on the rules of the copies. It must print one line for each
error, then one line with the count of the rules of the project, the count of the rules of the
copies and the count of errors, for example `0 specs, 89 upstream, 0 errors`. An error line
must start with `<path>:<line>: `. The line must be the line of the front matter key, of the
entry or of the reference that the error names, else 1. An error of a folder or of a missing
file must have only `<path>: `. The command must exit with 1 when it finds an error, else with
0. The command must not change a file and must not use the network. `spezi install` writes the
index `specs/README.md` (000007) and the block in `AGENTS.md` (000079) (000083).

Reason: CI and an agent run the same check with one command. The count of the copies shows
that the rules of the kit and of the other repositories are there. The project must not change
a copy (000048), so the check reports only what it needs to read the rules.

Test: `tests/test_check.py`.
