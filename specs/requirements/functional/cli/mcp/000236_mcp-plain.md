---
id: "000236"
title: The MCP server returns plain text
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# The MCP server returns plain text

The MCP server must return the plain text of each command (spec 000238).

Reason: An agent reads plain text, and a color code is noise for it.

Test: `tests/test_output.py`.
