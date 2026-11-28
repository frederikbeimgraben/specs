---
id: "000193"
title: An element without code has the path -
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
  - src/spezi/sections.py
scope:
  - specs/
---

# An element without code has the path -

An element without code, for example an external system, must have `-` as its path.

Reason: The table then shows that the element has no code, and the check skips it.

Test: `spezi check`.
