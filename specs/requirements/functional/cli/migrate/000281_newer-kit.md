---
id: "000281"
title: A copy that needs a newer kit stops the command
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_migrations.py:test_add_stops_for_a_newer_kit
implementation:
  - src/spezi/migrations/
  - src/spezi/kit.py
  - src/spezi/cli.py
  - src/spezi/install.py
scope:
  - src/spezi/
---

# A copy that needs a newer kit stops the command

A different repository can need a kit that the kit ref of the project does not hold. Then the
command must stop with an error and change no file. The error tells to run `spezi update`
first.

Reason: The copies of older repositories stay readable, and a newer copy waits for the kit.

Test: `tests/test_migrations.py`.
