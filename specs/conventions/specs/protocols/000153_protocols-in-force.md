---
id: "000153"
title: Each entry of protocols is in force
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# Each entry of protocols is in force

Each entry of `protocols` must name a protocol spec that is in force.

Reason: A reference to a replaced format points to a contract that the product no longer uses.

Test: `spezi check` checks every entry of `protocols`.
