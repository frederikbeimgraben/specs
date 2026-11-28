---
id: "000032"
title: A Python test checks its result with assert
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# A Python test checks its result with assert

A Python test must check its result with `assert`.

Reason: `pytest` shows the values of a failed `assert`.

Test: The ruff rules `PT009` and `PT027` find the checks of `unittest` (spec 000028). A review
finds the rest.
