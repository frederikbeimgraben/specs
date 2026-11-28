---
id: "000213"
title: spezi check prints the errors before the warnings
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

# spezi check prints the errors before the warnings

`spezi check` must print one line for each error, then one line for each warning
(spec 000093).

Reason: The errors are more important, so the reader sees them first.

Test: `tests/test_check.py`.
