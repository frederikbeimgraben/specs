---
id: "000095"
title: A command loads only the libraries that it needs
kind: non-functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_startup.py:test_a_command_loads_no_server_library
implementation:
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# A command loads only the libraries that it needs

A command other than `spezi mcp` must not load the Python packages `mcp`, `lsprotocol` and
`pygls`. Only `spezi mcp` must load `mcp`. Only `spezi lsp` must load `lsprotocol` and `pygls`.

Reason: These packages need more than 1 second to load. Each command, `spezi --help` too, then
starts slowly, and the tests start the command many times.

Test: `tests/test_startup.py:test_a_command_loads_no_server_library`.
