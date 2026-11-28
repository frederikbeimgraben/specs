---
id: "000013"
title: A conditional expression is nested at most one level
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# A conditional expression is nested at most one level

A conditional expression must not hold more than one level of conditional expressions in it.

Reason: A deeper conditional expression is difficult to read. A `match` (spec 000011) shows the
outcomes better.
