---
id: "000052"
title: A function body has one shape
kind: style
status: draft
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - src/specs_kit/
scope:
  - src/
---

# A function body has one shape

A function body must have this shape: guard checks that raise an error, then locals, then one
`return` of an expression or one `match` with one `return` in each case. The best body is
only one `return` of one expression.

Reason: A body of this shape has one path to its result. A reader and a type checker see each
outcome.
