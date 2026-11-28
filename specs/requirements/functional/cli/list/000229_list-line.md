---
id: "000229"
title: A line of spezi list has four columns
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/queries.py
  - src/spezi/cli.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# A line of spezi list has four columns

A line of `spezi list` must hold the kind letter, the short form (spec 000047), the status and
the title, in this order and separated by tabs. For example:

```text
S	github.com/frederikbeimgraben/spezi-python:000001	approved	Python code needs Python 3.13 or later
```

Reason: The short form is the form that code and specs use. The kind letter tells the kind
without the long path.

Test: `tests/test_queries.py`.
