---
id: "000154"
title: A reference to a rule of the same repository is the number
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# A reference to a rule of the same repository is the number

A reference to a rule of the same repository must be only the number, for example `000012`.

Reason: The number is the identity of a rule (spec 000013), so the reference stays the same
when a rule moves.

Test: `spezi check`.
