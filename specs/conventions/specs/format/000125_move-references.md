---
id: "000125"
title: A move changes every reference in the same pull request
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/
scope:
  - specs/
---

# A move changes every reference in the same pull request

A pull request that moves a spec file must change every reference to its long form in the same
pull request.

Reason: A long form names the path, and an old path points to nothing.
