---
id: "000019"
title: One rule controls one thing
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - specs/
scope:
  - specs/
---

# One rule controls one thing

One rule must control one behavior or one property. If a rule needs "and also", it must become
two rules.

Reason: A reference to a rule must point to one thing that is true or false.
