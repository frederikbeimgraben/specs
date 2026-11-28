---
id: "000310"
title: spezi remove stops for the kit and for an unknown repository
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_configure.py:test_remove_stops_for_the_kit
implementation:
  - src/spezi/kit.py
  - src/spezi/cli.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# spezi remove stops for the kit and for an unknown repository

`spezi remove` must stop with an error and change no file when `<repo>` is the kit or is not in
`spezi.toml`.

Reason: The project needs the templates and the migrations of the kit.

Test: `tests/test_configure.py`.
