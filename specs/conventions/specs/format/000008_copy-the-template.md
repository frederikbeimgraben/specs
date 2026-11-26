---
id: "000008"
title: A new spec starts as a copy of the template
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - specs/TEMPLATE.md
  - specs/TEMPLATE-protocol.md
  - specs/TEMPLATE-structure.md
  - specs/TEMPLATE-decision.md
scope:
  - specs/
---

# A new spec starts as a copy of the template

A new spec must start as a copy of its template:

| Kind | Template |
| --- | --- |
| `functional`, `non-functional`, `style`, `convention`, `workflow`, `agent` | `specs/TEMPLATE.md` |
| `protocol` | `specs/TEMPLATE-protocol.md` |
| `structure` | `specs/TEMPLATE-structure.md` |
| `decision` | `specs/TEMPLATE-decision.md` |

Reason: The template holds the keys in the correct order and the fixed sections.

Test: `scripts/check_specs.py` checks the result.
