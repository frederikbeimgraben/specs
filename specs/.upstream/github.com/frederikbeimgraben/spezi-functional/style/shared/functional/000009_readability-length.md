---
id: "000009"
title: An expression has at most 8 lines
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# An expression has at most 8 lines

An expression must have at most 8 lines. Code must split a longer expression into named locals
or a named helper function.

Reason: The goal of (spec 000001) is code that is easier to read, not one long expression.
