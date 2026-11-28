---
id: "000010"
title: A loop that only causes effects is a for statement
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# A loop that only causes effects is a for statement

A loop that only causes effects, for example a write to a file, must be a `for` statement. It
must not be a comprehension.

Reason: A comprehension whose result nobody reads hides the effect.
