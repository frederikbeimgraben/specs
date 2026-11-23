---
id: "000008"
title: A new spec starts as a copy of the template
kind: style
status: draft
owner: frederikbeimgraben
updated: 2026-11-23
implementation:
  - specs/TEMPLATE.md
  - specs/TEMPLATE-protocol.md
  - specs/TEMPLATE-structure.md
scope:
  - specs/
---

# A new spec starts as a copy of the template

A new spec must start as a copy of its template:

| Kind | Template |
| --- | --- |
| `functional`, `non-functional`, `style` | `specs/TEMPLATE.md` |
| `protocol` | `specs/TEMPLATE-protocol.md` |
| `structure` | `specs/TEMPLATE-structure.md` |

Reason: The template holds the keys in the correct order and the fixed sections.

Test: `scripts/check_specs.py` checks the result.
