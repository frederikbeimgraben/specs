---
id: "000264"
title: The menu comes back after each item
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/configure.py
  - src/spezi/settings.py
  - src/spezi/cli.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# The menu comes back after each item

After an item, `spezi configure` must show the menu (spec 000086) again. A change must stay in
memory until `save`.

Reason: A person changes many values and then saves them one time.

Test: `tests/test_configure.py`.
