---
id: "000227"
title: spezi list with a kind prints only this kind
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_queries.py:test_list_filters_by_kind
implementation:
  - src/spezi/queries.py
  - src/spezi/cli.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# spezi list with a kind prints only this kind

`spezi list <kind>` must print only the rules of this kind. `<kind>` is a kind or its letter
(spec 000004).

Reason: An agent finds the rules of one kind without a filter of its own.

Test: `tests/test_queries.py`.
