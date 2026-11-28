---
id: "000265"
title: save writes spezi.toml when the settings are correct
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_configure.py:test_the_menu_saves_the_changes
implementation:
  - src/spezi/configure.py
  - src/spezi/settings.py
  - src/spezi/cli.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# save writes spezi.toml when the settings are correct

When the settings break a rule (spec 000078, 000084), `save` in the menu of `spezi configure`
must show the error and the menu again. An example is `claude` on with `agents` off. Else `save`
must write `spezi.toml`.

Reason: A wrong setting never goes to the file.

Test: `tests/test_configure.py`.
