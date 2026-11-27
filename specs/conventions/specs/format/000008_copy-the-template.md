---
id: "000008"
title: A new spec starts as a copy of the template
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
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

`specs new <kind> <area>/<topic> <name> "<title>" --scope <path>` must make the copy (000069). It
sets the number, the title, the kind, the owner, the date and `scope`. The copy must pass
`specs check`.

Reason: The template holds the keys in the correct order and the fixed sections. The command
gives the next free number (000013), so that nobody must count by hand.

Test: `specs check` checks the result.
