---
id: "000163"
title: Nobody changes a file of a copy by hand
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/changes.py
  - src/spezi/check.py
  - src/spezi/kit.py
  - src/spezi/install.py
scope:
  - specs/
---

# Nobody changes a file of a copy by hand

A person or an agent must not change a file of a copy (spec 000048).

Reason: The next `spezi install` or `spezi update` removes the change. The hash in `spezi.lock`
shows it (spec 000082).

Test: `spezi check` fails when the hash of a copy is not the hash in `spezi.lock`.
