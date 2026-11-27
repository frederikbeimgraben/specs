---
id: "000059"
title: The exceptions of the functional style are named
kind: style
status: draft
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - src/specs_kit/
scope:
  - src/
---

# The exceptions of the functional style are named

The rules 000052 to 000058 must not apply to these parts:

- tests
- `try`, `with` and `raise`
- code that a library or the language needs in a different form

Reason: The library or the language needs them in this form.
