---
id: "000031"
title: A Python test file has the name test_<topic>.py
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# A Python test file has the name test_<topic>.py

A Python test file must have the name `test_<topic>.py`.

Reason: `pytest` finds a file with this name, and the name tells the topic of its tests.

Test: `pytest` finds the tests. A review checks the names of the files.
