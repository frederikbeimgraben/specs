---
id: "000024"
title: Python code builds a value with a comprehension
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# Python code builds a value with a comprehension

Python code must build a value with a list, set or dict comprehension, or with a generator
expression (spec github.com/frederikbeimgraben/spezi-functional:000005).

Reason: One fixed means for each rule makes the code of two agents look the same.

Test: The ruff rules `C4`, `PERF401` and `PERF402` find a loop that builds a value
(spec 000028). A review finds the rest.
