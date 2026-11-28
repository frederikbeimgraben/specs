---
id: "000217"
title: spezi check exits with 1 for an error
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/agents.py
  - src/spezi/check.py
  - src/spezi/index.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# spezi check exits with 1 for an error

`spezi check` must exit with 1 when it finds an error, else with 0.

Reason: CI fails on the exit code.

Test: `tests/test_check.py`.
