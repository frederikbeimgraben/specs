---
id: "000214"
title: The last line of spezi check counts the rules and the findings
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

# The last line of spezi check counts the rules and the findings

The last line of `spezi check` must count the rules of the project, the rules of the copies, the
errors and the warnings. For example: `0 specs, 89 upstream, 0 errors, 0 warnings`.

Reason: The count of the copies shows that the rules of the kit and of the other repositories
are there.

Test: `tests/test_check.py`.
