---
id: "000035"
title: Each element of the diagram has a row in the element table
kind: style
status: draft
owner: frederikbeimgraben
updated: 2026-11-23
implementation:
  - scripts/check_specs.py
scope:
  - specs/
---

# Each element of the diagram has a row in the element table

`## Elements` must hold one table with the columns `Element`, `Path` and `Meaning`. Each row
must name one element of the diagram with the name that the diagram uses. Each element of the
diagram must have one row. `Meaning` must tell in one sentence what the element is.

Reason: The table is the text alternative of the diagram. A screen reader, a search and an
agent read the table when they cannot read the drawing.

Test: `scripts/check_specs.py`: each name of the table occurs in the diagram. For `class`,
`state`, `sequence` and `entity` it also finds each element of the diagram in the table.
