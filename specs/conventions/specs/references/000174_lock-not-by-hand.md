---
id: "000174"
title: Nobody changes spezi.lock by hand
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/lock.py
  - src/spezi/check.py
  - src/spezi/kit.py
scope:
  - src/spezi/lock.py
  - spezi.toml
---

# Nobody changes spezi.lock by hand

A person or an agent must not change `spezi.lock` (spec 000082).

Reason: The check then finds a copy that a person changed.

Test: `spezi check` fails when a file of a copy changes.
