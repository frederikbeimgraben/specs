---
id: "000033"
title: A Python test is not in a class
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# A Python test is not in a class

A Python test must not be in a class.

Reason: A test function needs no class, and a spec names it as `<file>:<function>`.

Test: A review finds a test in a class.
