---
id: "000107"
title: A spec uses one word for one thing
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/
scope:
  - specs/
---

# A spec uses one word for one thing

A spec must use one word for one thing.

Reason: Two words make the reader look for two things (spec 000025).

Test: `spezi check` gives a warning for two verbs of one group in one rule (spec 000093).
