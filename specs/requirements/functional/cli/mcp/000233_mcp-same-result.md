---
id: "000233"
title: An MCP tool gives the result of its command
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_output.py:test_mcp_tools_give_the_plain_results
implementation:
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# An MCP tool gives the result of its command

Each tool of the MCP server (spec 000074) must give the same result as the command of the same
name.

Reason: An agent gets the same answer through the shell and through MCP.

Test: `tests/test_output.py`.
