---
id: "000035"
title: Each element of the diagram has a row in the element table
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

# Each element of the diagram has a row in the element table

`## Elements` must hold one table with the columns `Element`, `Path` and `Meaning`.

Reason: The table is the text alternative of the diagram. A screen reader, a search and an
agent read the table when they cannot read the drawing.

Test: `spezi check`.
