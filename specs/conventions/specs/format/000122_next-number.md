---
id: "000122"
title: A new rule gets the highest number plus one
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
  - spezi.toml
scope:
  - specs/
---

# A new rule gets the highest number plus one

A new rule must get the highest number of the branch and of the base branch, plus one.
`base_ref` in `spezi.toml` names the base branch (spec 000078).

Reason: The command `spezi new` gives this number (spec 000069), so that nobody counts by hand.

Test: `tests/test_new.py`.
