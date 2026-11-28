---
id: "000074"
title: spezi mcp runs the MCP server
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# spezi mcp runs the MCP server

`spezi mcp` must run an MCP server with the name `spezi` on stdin and stdout. The server must
have the tools `check`, `install`, `resolve`, `show`, `list`, `search`, `new`, `configure` and
`remove`.

Reason: An agent uses the specs without a shell.

Test: `tests/test_output.py`.
