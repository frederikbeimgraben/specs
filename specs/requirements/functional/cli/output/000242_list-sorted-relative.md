---
id: "000242"
title: The list of files is sorted by relative path
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_output.py:test_changed_files_are_sorted_and_relative
implementation:
  - src/spezi/changes.py
  - src/spezi/cli.py
  - src/spezi/view.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# The list of files is sorted by relative path

Each path of the list of changed files (spec 000077) must be relative to the root of the
project. The list must be sorted by path.

Reason: The list is the same on each computer and for each run.

Test: `tests/test_output.py`.
