---
id: "000008"
title: A new spec starts as a copy of the template
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/.templates/TEMPLATE.md
  - specs/.templates/TEMPLATE-protocol.md
  - specs/.templates/TEMPLATE-structure.md
  - specs/.templates/TEMPLATE-decision.md
scope:
  - specs/
---

# A new spec starts as a copy of the template

A new spec must start as a copy of its template in `specs/.templates/`:

| Kind | Template |
| --- | --- |
| `functional`, `non-functional`, `style`, `convention`, `workflow`, `agent` | `specs/.templates/TEMPLATE.md` |
| `protocol` | `specs/.templates/TEMPLATE-protocol.md` |
| `structure` | `specs/.templates/TEMPLATE-structure.md` |
| `decision` | `specs/.templates/TEMPLATE-decision.md` |

Reason: The template holds the keys in the right order and the sections of the kind.

Test: `spezi check` checks the result.
