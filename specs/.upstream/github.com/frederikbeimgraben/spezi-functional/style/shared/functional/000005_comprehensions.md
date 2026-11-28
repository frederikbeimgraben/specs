---
id: "000005"
title: Comprehensions instead of loops
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# Comprehensions instead of loops

A loop that builds a value must be a comprehension, a generator expression, or a `map`,
`filter` or `reduce`.

Reason: A comprehension shows the value that it builds in one place.
