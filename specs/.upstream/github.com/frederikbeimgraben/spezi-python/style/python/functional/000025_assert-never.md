---
id: "000025"
title: A match that the type checker cannot see as exhaustive ends with assert_never
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# A match that the type checker cannot see as exhaustive ends with assert_never

A `match` must end with a case that calls `assert_never` from `typing` when the type checker
cannot see that the `match` is exhaustive (spec github.com/frederikbeimgraben/spezi-functional:000006).

Reason: The type checker then shows an error for each value that has no case.

Test: `reportMatchNotExhaustive` of basedpyright.
