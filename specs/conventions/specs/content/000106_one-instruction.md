---
id: "000106"
title: One sentence holds one instruction
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/
scope:
  - specs/
---

# One sentence holds one instruction

A spec must write one instruction in one sentence.

Reason: A reader then finds each instruction alone (spec 000025).

Test: `spezi check` gives a warning for a sentence with two instructions (spec 000093).
