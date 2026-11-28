---
id: "000216"
title: An error of a folder names only the path
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

# An error of a folder names only the path

An error of a folder or of a missing file must start with `<path>: `, without a line.

Reason: A folder or a missing file has no line.

Test: `tests/test_check.py`.
