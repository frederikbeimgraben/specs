---
id: "000058"
title: Data types are frozen by default
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
implementation:
  - src/spezi/
scope:
  - src/
---

# Data types are frozen by default

A data type must be immutable unless a write needs it. Its collection fields must be
immutable collections too.

Reason: 000055 needs data that cannot change.
