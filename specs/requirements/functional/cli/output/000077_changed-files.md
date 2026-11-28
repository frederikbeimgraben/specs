---
id: "000077"
title: spezi lists the files that a command changes
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/changes.py
  - src/spezi/cli.py
  - src/spezi/view.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# spezi lists the files that a command changes

Each command of `spezi` that changes files must list each file that it created, changed or
deleted, one file on each line, as in `git status --short`. These commands are `init`,
`install`, `update`, `add`, `configure`, `remove`, `new` and `setup-ide`.

| Mark | Change | Color on a terminal |
| --- | --- | --- |
| `A` | The command created the file. | Green |
| `M` | The command changed the content of the file. | Yellow |
| `D` | The command deleted the file. | Red |

Reason: The person sees what a command did without `git status`, and a script can read the
list.

Test: `tests/test_output.py`.
