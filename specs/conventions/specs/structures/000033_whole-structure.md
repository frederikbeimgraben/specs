---
id: "000033"
title: A structure spec has fixed sections
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
  - src/spezi/sections.py
  - specs/.templates/TEMPLATE-structure.md
scope:
  - specs/
---

# A structure spec has fixed sections

The body of a structure spec must have the `#` title, the rule text and then exactly these `##`
sections, in this order:

| Section | Content |
| --- | --- |
| `## Diagram` | One Mermaid code block (spec 000034). |
| `## Elements` | One table with one row for each element of the diagram (spec 000035). |

Reason: The reader sees the structure and the rule that binds it in one file.

Test: `spezi check` checks the headings and their order.
