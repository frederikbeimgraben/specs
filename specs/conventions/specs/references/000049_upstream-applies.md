---
id: "000049"
title: Each rule of a different repository applies unless a project rule replaces it
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# Each rule of a different repository applies unless a project rule replaces it

Each rule of a copy of 000048 with the status `draft` or `approved` must apply to the project.
A rule that must not apply must be in `replaces` of a project rule with the status `draft` or
`approved`. A rule that the project drops without a new rule must be in `replaces` of a decision
spec (000042). A reference must not point to a replaced rule.

Reason: A new rule of the different repository applies after the next update. The project rule
that replaces it holds the reason, and the owner approves it like each other rule.

Test: `spezi check` checks that each entry of `replaces` exists in the copy and that
no reference points to a replaced rule.
