---
id: "000007"
title: Data types are frozen by default
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# Data types are frozen by default

A data type must be immutable unless a write needs it. Its collection fields must be
immutable collections too.

Reason: 000004 needs data that cannot change.
