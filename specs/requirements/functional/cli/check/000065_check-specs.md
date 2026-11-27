---
id: "000065"
title: specs check checks the specs
kind: functional
status: draft
owner: frederikbeimgraben
updated: 2026-11-27
tests:
  - tests/test_check.py:test_check_passes_after_init
  - tests/test_check.py:test_check_changes_no_file
  - tests/test_check.py:test_install_writes_the_index
  - tests/test_check.py:test_check_finds_a_rule_without_must
  - tests/test_check.py:test_check_finds_a_bad_file_name
  - tests/test_check.py:test_check_finds_a_missing_key
  - tests/test_check.py:test_check_finds_a_stale_index
implementation:
  - src/specs_kit/agents.py
  - src/specs_kit/check.py
  - src/specs_kit/index.py
  - src/specs_kit/cli.py
scope:
  - src/specs_kit/
---

# specs check checks the specs

`specs check` must run every check of the conventions on the specs of the project. It must also
check that `specs.toml`, `specs.lock` and the copies of 000048 agree (000082), and check each `§` reference in
`code_dirs` (000017). It must print one line for each
error, then the count of specs and errors. It must exit with 1 when it finds an error, else
with 0. The command must not change a file and must not use the network. `specs install`
writes the index `specs/README.md` (000007) and the block in `AGENTS.md` (000079) (000083).

Reason: CI and an agent run the same check with one command.

Test: `tests/test_check.py`.
