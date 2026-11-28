---
id: "000136"
title: Nobody changes the index by hand
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
  - src/spezi/index.py
scope:
  - specs/
---

# Nobody changes the index by hand

A person or an agent must not change the index `specs/README.md` by hand (spec 000007).

Reason: `spezi install` writes the index again and removes each change by hand.

Test: `spezi check` fails when `specs/README.md` is not current.
