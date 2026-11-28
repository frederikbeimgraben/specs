---
id: "000009"
title: A Python test is a function test_<behavior>
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# A Python test is a function test_<behavior>

A Python test must be a function with the name `test_<behavior>`.

Reason: A function with a name for its behavior is the smallest test, and a spec can name it as
`<file>:<function>`.

Test: A review checks the names of the tests.
