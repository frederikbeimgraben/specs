---
id: "000190"
title: Each element of the diagram has a row
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

# Each element of the diagram has a row

Each element of the diagram must have one row in `## Elements` (spec 000035).

Reason: The table is complete only with each element.

Test: For `class`, `state`, `sequence` and `entity`, `spezi check` finds each element of the
diagram in the table.
