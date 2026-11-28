---
id: "000114"
title: Each path of the front matter exists
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
  - src/spezi/project.py
scope:
  - specs/
---

# Each path of the front matter exists

Each path in `tests`, `implementation` and `scope` must exist, as a path from the repository
root.

Reason: A path that does not exist points the reader to nothing.

Test: `spezi check`.
