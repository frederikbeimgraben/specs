---
id: "000104"
title: A description has at most 25 words
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/
scope:
  - specs/
---

# A description has at most 25 words

A description in a spec must have at most 25 words.

Reason: ASD-STE100 sets this limit, because a short sentence is clear (spec 000025).

Test: `spezi check` gives a warning for a sentence with more than 25 words (spec 000093).
