---
id: "000189"
title: A row names one element with its name in the diagram
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

# A row names one element with its name in the diagram

Each row of `## Elements` (spec 000035) must name one element of the diagram with the name that
the diagram uses.

Reason: A search finds the element in the diagram and in the table.

Test: `spezi check`: each name of the table occurs in the diagram.
