---
id: "000021"
title: A closed set of values is an Enum or a Literal
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# A closed set of values is an Enum or a Literal

A closed set of values must be an `Enum` or a `Literal`.

Reason: The type checker then finds a value that is not in the set.

Test: A review finds a closed set of values as plain strings or numbers.
