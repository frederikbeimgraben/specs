---
id: "000194"
title: A structure spec lists its element paths in implementation
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/
scope:
  - specs/
---

# A structure spec lists its element paths in implementation

A structure spec with an element path must list the same paths, or their folders, in
`implementation`.

Reason: A tool finds the structure specs of a changed file.

Test: Review.
