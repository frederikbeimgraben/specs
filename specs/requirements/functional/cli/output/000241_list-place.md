---
id: "000241"
title: The list of files comes before the report of the check
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_output.py:test_the_report_comes_after_the_files
implementation:
  - src/spezi/changes.py
  - src/spezi/cli.py
  - src/spezi/view.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# The list of files comes before the report of the check

The list of changed files (spec 000077) must come after the message and the hints, and before
the report of `spezi check`. A command without a check must end with the list.

Reason: The report of the check is then at the end.

Test: `tests/test_output.py`.
