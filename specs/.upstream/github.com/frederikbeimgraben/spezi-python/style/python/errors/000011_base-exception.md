---
id: "000011"
title: A Python package has one base exception class
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# A Python package has one base exception class

A Python package must have one base class for its own exceptions, for example `KitError`.

Reason: A caller catches each expected error of the package with one class.

Test: A review checks the exception classes.
