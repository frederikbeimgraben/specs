---
id: "000012"
title: A branch with two outcomes is a conditional expression
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# A branch with two outcomes is a conditional expression

A branch on one value with exactly two outcomes must be a conditional expression.

Reason: A conditional expression gives the value in one line, and a `match` for two outcomes
adds lines without a gain.
