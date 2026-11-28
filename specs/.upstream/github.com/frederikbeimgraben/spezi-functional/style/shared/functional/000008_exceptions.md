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

The rules of the functional style must not apply to the parts of the list below. These rules are
(spec 000001, 000002, 000003, 000004, 000005, 000006, 000007, 000009, 000011, 000012, 000013, 000014).

- Tests.
- `try`, `with` and `raise`.
- A `for` statement that only causes effects (spec 000010).
- Code that a library or the language needs in a different form.

Reason: The library or the language needs these parts in this form. An effect needs a
statement.
