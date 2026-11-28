---
id: "000065"
title: spezi check checks the specs
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_check.py:test_check_passes_after_init
  - tests/test_check.py:test_install_writes_the_index
  - tests/test_check.py:test_check_finds_a_rule_without_must
  - tests/test_check.py:test_check_finds_a_bad_file_name
  - tests/test_check.py:test_check_finds_a_missing_key
  - tests/test_check.py:test_check_finds_a_stale_index
  - tests/test_check.py:test_check_finds_a_file_outside_the_kind_folders
  - tests/test_check.py:test_check_finds_an_old_diagram_type
  - tests/test_check.py:test_check_finds_front_matter_that_is_no_yaml
implementation:
  - src/spezi/agents.py
  - src/spezi/check.py
  - src/spezi/index.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# spezi check checks the specs

`spezi check` must run every check of the conventions on the specs of the project.

Reason: CI and an agent run the same check with one command.

Test: `tests/test_check.py`.
