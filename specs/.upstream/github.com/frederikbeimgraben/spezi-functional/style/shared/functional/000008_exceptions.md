---
id: "000008"
title: The exceptions of the functional style are named
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# The exceptions of the functional style are named

The rules 000001 to 000007 must not apply to these parts:

- tests
- `try`, `with` and `raise`
- code that a library or the language needs in a different form

Reason: The library or the language needs them in this form.
