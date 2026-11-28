---
id: "000226"
title: resolve and show stop for an unknown ID
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_queries.py:test_resolve_stops_for_an_unknown_id
  - tests/test_queries.py:test_show_stops_for_an_unknown_id
implementation:
  - src/spezi/queries.py
  - src/spezi/project.py
scope:
  - src/spezi/
---

# resolve and show stop for an unknown ID

`spezi resolve` and `spezi show` must stop with an error when no rule of the project or of a copy
has the ID.

Reason: An empty result looks like a rule without text.

Test: `tests/test_queries.py`.
