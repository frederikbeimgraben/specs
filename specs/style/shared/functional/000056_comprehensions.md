---
id: "000056"
title: Comprehensions instead of loops
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
implementation:
  - src/spezi/
scope:
  - src/
---

# Comprehensions instead of loops

A loop that builds a value must be a comprehension, a generator expression, or a `map`,
`filter` or `reduce`. A loop that only causes effects, for example a write to a file, must stay
a `for` statement.

Reason: A comprehension shows the value that it builds in one place. A comprehension whose
result nobody reads hides the effect.
