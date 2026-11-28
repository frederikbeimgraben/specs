---
id: "000268"
title: spezi configure stops for a bad key or value
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_configure.py:test_configure_stops_for_a_bad_value
  - tests/test_configure.py:test_configure_stops_for_claude_without_agents
implementation:
  - src/spezi/configure.py
  - src/spezi/settings.py
  - src/spezi/cli.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# spezi configure stops for a bad key or value

`spezi configure <key> <value>` must stop with an error and change no file in these cases:

- `<key>` is not a key of `configure-key` (spec 000267).
- `<value>` has a different form.
- The value breaks a rule (spec 000078, 000084).

Reason: A wrong value never goes to the file.

Test: `tests/test_configure.py`.
