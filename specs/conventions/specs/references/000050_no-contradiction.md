---
id: "000050"
title: A rule of the project does not contradict a rule of a different repository
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/
scope:
  - specs/
---

# A rule of the project does not contradict a rule of a different repository

A rule of the project must not contradict a rule of a copy (spec 000048) that applies
(spec 000049). A project that needs a different rule replaces the rule of the copy
(spec 000168).

Reason: Every agent must know which of the two rules applies. `replaces` makes this a decision
that the owner approves.

Test: Review.
