---
id: "000003"
title: A local is bound once
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# A local is bound once

A local name must get exactly one assignment. Code must not assign a new value to a name. It
must not use `+=`, a counter or a flag that a branch sets. A reader must be able to read each
local as a constant.

Reason: A name with one value has one meaning in the whole function.
