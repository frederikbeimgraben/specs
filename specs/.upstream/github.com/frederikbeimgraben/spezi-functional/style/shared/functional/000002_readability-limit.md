---
id: "000002"
title: An expression is at most three levels deep
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# An expression is at most three levels deep

An expression must be at most three levels deep. Code must split a deeper expression into
named locals or a named helper function.

Reason: The goal of (spec 000001) is code that is easier to read, not one long expression.
