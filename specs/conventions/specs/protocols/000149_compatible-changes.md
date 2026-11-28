---
id: "000149"
title: Only two changes of a format are compatible
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/
scope:
  - specs/
---

# Only two changes of a format are compatible

A change of a format must count as compatible only when it is one of these changes:

- A new optional key in an object.
- A new value in a list of values, if `## Compatibility` tells the receiver to ignore an
  unknown value.

All other changes are breaking changes (spec 000030).

Reason: A receiver that obeys `## Compatibility` reads these changes without an error.

Test: Review.
