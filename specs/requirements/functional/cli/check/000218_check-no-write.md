---
id: "000218"
title: spezi check changes no file
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_check.py:test_check_changes_no_file
implementation:
  - src/spezi/agents.py
  - src/spezi/check.py
  - src/spezi/index.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# spezi check changes no file

`spezi check` must not change a file.

Reason: CI and an agent can run the check at each time without a change of the project.

Test: `tests/test_check.py`.
