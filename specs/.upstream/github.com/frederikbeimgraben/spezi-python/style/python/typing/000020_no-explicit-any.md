---
id: "000020"
title: Python code uses no explicit Any
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# Python code uses no explicit Any

Python code must not use `Any` as a type.

Reason: `Any` turns off the type checker for the value (spec 000002).

Test: `reportExplicitAny` of basedpyright.
