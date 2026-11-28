---
id: "000017"
title: A name that a module does not export starts with _
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# A name that a module does not export starts with _

A name that a module does not give to other modules must start with `_`.

Reason: `_` tells that the name is not part of the interface of the module.

Test: A review checks the names with and without `_`.
