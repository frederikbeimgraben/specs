---
id: "000269"
title: spezi configure needs a terminal or a key
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_configure.py:test_configure_needs_a_terminal_or_a_key
implementation:
  - src/spezi/configure.py
  - src/spezi/settings.py
  - src/spezi/cli.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# spezi configure needs a terminal or a key

Without a terminal, or with `-y`, `spezi configure` must stop with an error when it has no key and
value.

Reason: The menu needs a person at a terminal.

Test: `tests/test_configure.py`.
