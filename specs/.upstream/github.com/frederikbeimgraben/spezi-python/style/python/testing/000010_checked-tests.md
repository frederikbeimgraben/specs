---
id: "000010"
title: The code checks also apply to the tests
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# The code checks also apply to the tests

These rules must also apply to the code in `tests/`:
(spec 000002, 000003, 000005, 000006, 000020, 000021, 000022, 000028, 000029, 000030).

Reason: Tests are code. One set of tools then checks all code.

Test: `basedpyright` and `ruff` check `tests/`.
