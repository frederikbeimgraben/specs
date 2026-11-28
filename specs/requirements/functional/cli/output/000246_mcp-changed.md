---
id: "000246"
title: The MCP tools return the list of files
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

# The MCP tools return the list of files

The MCP tools `install`, `new`, `configure` and `remove` must return the list of changed files
(spec 000077) as plain text, in the same place as the command.

Reason: An agent sees what the tool changed.

Test: Review.
