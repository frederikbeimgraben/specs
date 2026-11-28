---
id: "000250"
title: An object of changed has a mark and a path
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_json.py:test_a_command_that_changes_files_gives_all_parts
implementation:
  - src/spezi/data.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# An object of changed has a mark and a path

Each object of `changed` in the JSON output (spec 000080) must hold `mark` and `path`
(spec 000077).

Reason: A script reads the changed files without the text form.

Test: `tests/test_json.py`.
