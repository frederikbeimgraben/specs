---
id: "000235"
title: Five MCP tools write no file
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# Five MCP tools write no file

The MCP tools `check`, `resolve`, `show`, `list` and `search` must not write a file.

Reason: An agent can call them at each time without a change of the project.

Test: Review.
