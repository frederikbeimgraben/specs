---
id: "000002"
title: Python code is strictly typed
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# Python code is strictly typed

Every function must have a type for each parameter and for its return value. Code must not use
a bare `Any`. A closed set of values must be an `Enum` or a `Literal`. basedpyright must report
0 errors with the settings in `pyproject.toml`.

Reason: The type checker finds an error before a test or a user does.

Test: `basedpyright`.
