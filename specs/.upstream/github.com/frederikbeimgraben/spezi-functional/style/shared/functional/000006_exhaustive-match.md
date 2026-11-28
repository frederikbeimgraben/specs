---
id: "000006"
title: A match is exhaustive
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# A match is exhaustive

A `match` must have a case for each value of its subject.

Reason: The type checker finds a case that the code forgot.
