---
id: "000014"
title: A moved rule keeps its number
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - specs/
scope:
  - specs/
---

# A moved rule keeps its number

If a file moves to a different folder, the path part of its ID changes. The number and the file
name must not change. Every reference must change in the same pull request.

Reason: The number is the identity of a rule (spec 000013).
