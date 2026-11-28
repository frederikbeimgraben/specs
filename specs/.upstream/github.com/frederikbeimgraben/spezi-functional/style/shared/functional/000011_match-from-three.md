---
id: "000011"
title: A branch with three or more outcomes is a match
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# A branch with three or more outcomes is a match

A branch on one value with three or more outcomes must be a `match`. It must not be a chain of
`if`, `elif` and `else`.

Reason: A `match` shows each outcome at the same level, and the type checker can check it
(spec 000006).
