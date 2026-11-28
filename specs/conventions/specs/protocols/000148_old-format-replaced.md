---
id: "000148"
title: The old format is replaced when the product drops it
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/
scope:
  - specs/
---

# The old format is replaced when the product drops it

The old protocol spec of a breaking change (spec 000030) must get `status: replaced` when the
product no longer sends or reads the old format.

Reason: The status shows which format is in force.

Test: Review.
