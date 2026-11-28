---
id: "000124"
title: A number is never used again
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/
scope:
  - specs/
---

# A number is never used again

A new rule must not get the number of a different rule. This includes a rule with the status
`removed` or `replaced`.

Reason: An old reference must not point to a different rule.

Test: Review.
