---
id: "000006"
title: A branch on one value is an exhaustive match
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# A branch on one value is an exhaustive match

A branch on one value with two or more outcomes must be a `match`, not a chain of `if`,
`elif` and `else`. Every case must have a `return`. The match must be exhaustive. A choice
between two values must be a conditional expression, nested at most one level.

Reason: The type checker finds a case that the code forgot.
