---
id: "000234"
title: The MCP tool configure takes a key and a value
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# The MCP tool configure takes a key and a value

The MCP tool `configure` must take a key and a value, as `spezi configure <key> <value>` does
(spec 000086).

Reason: An MCP tool cannot show a menu.

Test: Review.
