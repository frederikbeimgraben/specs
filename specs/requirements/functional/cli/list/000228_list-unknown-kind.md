---
id: "000228"
title: spezi list stops for an unknown kind
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

# spezi list stops for an unknown kind

`spezi list <kind>` must stop with an error for an unknown kind.

Reason: An empty list looks like a kind without rules.

Test: Review.
