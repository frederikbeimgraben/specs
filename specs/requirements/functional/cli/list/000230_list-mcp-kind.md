---
id: "000230"
title: The MCP tool list takes an optional kind
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

# The MCP tool list takes an optional kind

The MCP tool `list` must take `kind` as an optional argument.

Reason: An agent filters by kind as with `spezi list <kind>` (spec 000227).

Test: Review.
