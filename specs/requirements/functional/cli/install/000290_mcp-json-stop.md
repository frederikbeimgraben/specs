---
id: "000290"
title: spezi install stops for a broken .mcp.json
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_install.py:test_install_stops_for_a_broken_mcp_file
  - tests/test_install.py:test_install_stops_for_mcp_servers_that_are_no_object
implementation:
  - src/spezi/install.py
  - src/spezi/kit.py
  - src/spezi/cli.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# spezi install stops for a broken .mcp.json

`spezi install` must stop with an error that names `.mcp.json` and keep `.mcp.json` as it is in
these cases:

- `.mcp.json` is no valid JSON.
- `.mcp.json` is not a JSON object.
- `.mcp.json` has a `mcpServers` that is not an object.

Reason: The command never writes over a file that it cannot read.

Test: `tests/test_install.py`.
