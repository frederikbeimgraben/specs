---
id: "000200"
title: A replaced or removed spec stays out of force
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/conventions/specs/format/000010_status.md
scope:
  - specs/
---

# A replaced or removed spec stays out of force

A spec with the status `replaced` or `removed` must not go back to `draft` or `approved`
(spec 000041).

Reason: A reference to a rule that left force must not change its meaning later.

Test: Review.
