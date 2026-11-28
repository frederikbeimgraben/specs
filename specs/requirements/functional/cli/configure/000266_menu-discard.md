---
id: "000266"
title: discard and Ctrl+C stop without a change
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_configure.py:test_the_menu_discards_the_changes
implementation:
  - src/spezi/configure.py
  - src/spezi/settings.py
  - src/spezi/cli.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# discard and Ctrl+C stop without a change

`discard` in the menu of `spezi configure` must ask one time when a value changed. It must then
stop without a change. Ctrl+C must also stop without a change.

Reason: A person can leave the menu at each time.

Test: `tests/test_configure.py`.
