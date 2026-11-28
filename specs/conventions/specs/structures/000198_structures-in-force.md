---
id: "000198"
title: Each entry of structures is in force
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# Each entry of structures is in force

Each entry of `structures` must name a structure spec that is in force.

Reason: A reference to a replaced structure points to old code.

Test: `spezi check` checks every entry of `structures`.
