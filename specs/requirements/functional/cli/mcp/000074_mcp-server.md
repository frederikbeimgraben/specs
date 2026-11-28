---
id: "000074"
title: spezi mcp runs the MCP server
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
tests:
  - tests/test_output.py:test_mcp_tools_give_the_plain_results
implementation:
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# spezi mcp runs the MCP server

`spezi mcp` must run an MCP server with the name `spezi` on stdin and stdout. The server must
have the tools `check`, `install`, `resolve`, `show`, `list`, `search`, `new`, `configure` and
`remove`. Each tool must give the same result as the command of the same name. The tool
`configure` takes a key and a value, as `spezi configure <key> <value>` does (000086). Only
`install`, `new`, `configure` and `remove` must write a file. `check` must not write the index.

Reason: An agent uses the specs without a shell.

Test: `tests/test_output.py`.
