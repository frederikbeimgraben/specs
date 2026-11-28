---
id: "000072"
title: spezi list prints every rule
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_queries.py:test_list_prints_one_line_for_each_rule
implementation:
  - src/spezi/queries.py
  - src/spezi/cli.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# spezi list prints every rule

`spezi list` must print one line for each rule of the project, then one line for each rule of
the copies.

Reason: An agent sees all rules in one call.

Test: `tests/test_queries.py`.
