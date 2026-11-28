---
id: "000212"
title: spezi check runs no convention check on a copy
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

# spezi check runs no convention check on a copy

`spezi check` must not run the checks of the conventions on the rules of the copies. It only
reads them (spec 000211).

Reason: The repository of a copy checks its own rules. The project cannot fix them.

Test: `tests/test_check.py`.
