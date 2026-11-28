---
id: "000001"
title: A function body has one shape
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# A function body has one shape

A function body must have these parts, in this order:

1. Guard checks that raise an error.
2. Locals.
3. One `return` of an expression, or one `match` with one `return` in each case.

Reason: A body of this shape has one path to its result. A reader and a type checker see each
outcome. The best body is only one `return` of one expression.
