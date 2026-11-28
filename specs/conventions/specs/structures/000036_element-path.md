---
id: "000036"
title: An element names the code that holds it
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
  - src/spezi/sections.py
scope:
  - specs/
---

# An element names the code that holds it

`Path` must be the file or the folder that holds the element, as a path from the repository
root.

Reason: A reader goes from the diagram to the code in one step.

Test: Review.
