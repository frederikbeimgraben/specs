---
id: "000170"
title: A reference does not point to a replaced rule
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# A reference does not point to a replaced rule

A reference must not point to a replaced rule of a copy (spec 000168).

Reason: The replaced rule does not apply to the project.

Test: `spezi check` checks that no reference points to a replaced rule.
