---
id: "000123"
title: The later pull request gives its specs new numbers
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

# The later pull request gives its specs new numbers

When two pull requests hold the same number, the pull request that merges later must give its
specs new numbers before its merge.

Reason: A number must stay unique (spec 000013), and the base branch knows only the merged numbers.

Test: `spezi check`: no spec of a branch has a number that the base branch gave to a different
spec after the branch left it.
