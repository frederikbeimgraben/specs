---
id: "000014"
title: The collection fields of a data type are immutable
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# The collection fields of a data type are immutable

Each collection field of a data type must be an immutable collection.

Reason: An immutable data type with a mutable list in it can still change (spec 000004).
