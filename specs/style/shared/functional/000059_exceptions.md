---
id: "000059"
title: The exceptions of the functional style are named
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
implementation:
  - src/spezi/
scope:
  - src/
---

# The exceptions of the functional style are named

The rules (spec 000052, 000053, 000054, 000055, 000056, 000057, 000058) must not apply to
these parts:

- tests
- `try`, `with` and `raise`
- code that a library or the language needs in a different form

Reason: The library or the language needs them in this form.
