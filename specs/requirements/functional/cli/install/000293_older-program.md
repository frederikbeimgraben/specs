---
id: "000293"
title: An older program stops the command
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/install.py
  - src/spezi/kit.py
  - src/spezi/cli.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# An older program stops the command

`spezi install`, `spezi update` and `spezi add` must stop with an error when this program is an
older commit of the kit than the kit commit in `spezi.lock`.

Reason: An older program does not know the migrations and the rules of the newer kit.

Test: `tests/test_migrations.py`.
