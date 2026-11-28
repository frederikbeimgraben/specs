---
id: "000004"
title: Python code binds a local once
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# Python code binds a local once

Python code must not use `+=` or a second assignment to a local
(spec github.com/frederikbeimgraben/spezi-functional:000003).

Reason: One fixed means for each rule makes the code of two agents look the same.

Test: The ruff rule `PLW2901` finds a loop variable with a new value (spec 000028). A review
finds the rest.
