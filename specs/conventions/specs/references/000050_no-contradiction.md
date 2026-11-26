---
id: "000050"
title: A rule of the project does not contradict a rule of a different repository
kind: convention
status: draft
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - specs/
scope:
  - specs/
---

# A rule of the project does not contradict a rule of a different repository

A rule of the project must not contradict a rule of a copy of 000048 that applies (000049). If
the project needs a different rule, the project rule must name the rule of the copy in
`replaces` (000049). An agent
that finds a contradiction must tell the owner (000001).

Reason: Every agent must know which of the two rules applies. `replaces` makes this a decision
that the owner approves.

Test: Review.
