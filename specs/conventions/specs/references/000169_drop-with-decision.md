---
id: "000169"
title: A decision spec drops a rule of a copy
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# A decision spec drops a rule of a copy

A rule of a copy that the project drops without a new rule must be in `replaces` of a decision
spec (spec 000042).

Reason: The decision spec holds the reason for the drop.

Test: Review.
