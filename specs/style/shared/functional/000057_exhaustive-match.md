---
id: "000057"
title: A branch on one value is an exhaustive match
kind: style
status: draft
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - src/specs_kit/
scope:
  - src/
---

# A branch on one value is an exhaustive match

A branch on one value with two or more outcomes must be a `match`, not a chain of `if`,
`elif` and `else`. Every case must have a `return`. The match must be exhaustive. A choice
between two values must be a conditional expression, nested at most one level.

Reason: The type checker finds a case that the code forgot.
