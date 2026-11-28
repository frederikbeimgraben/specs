---
id: "000270"
title: spezi configure keeps the other text of spezi.toml
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_configure.py:test_configure_keeps_the_comments
implementation:
  - src/spezi/configure.py
  - src/spezi/settings.py
  - src/spezi/cli.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# spezi configure keeps the other text of spezi.toml

`spezi configure` must change only the values in `spezi.toml`. The comments, the order of the
keys and the lines that it does not change must stay.

Reason: The comments of a person stay.

Test: `tests/test_configure.py`.
