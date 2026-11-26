---
id: "000034"
title: The diagram is one Mermaid block of a fixed type
kind: convention
status: draft
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - scripts/check_specs.py
scope:
  - specs/
---

# The diagram is one Mermaid block of a fixed type

`## Diagram` must hold exactly one fenced code block with the language `mermaid`. The first
line of the block must name the diagram type of the key `diagram`:

| `diagram` | First line | Use |
| --- | --- | --- |
| `class` | `classDiagram` | Classes, models and their relations. |
| `state` | `stateDiagram-v2` | The states and the transitions of one life cycle. |
| `sequence` | `sequenceDiagram` | The messages between parts, in time order. |
| `entity` | `erDiagram` | Tables, their columns and their relations. |
| `component` | `flowchart` | Components, services and their connections. |

The block must not hold styles, colors or click actions: no `style`, `classDef`, `linkStyle`,
`click`, `cssClass` or `:::`.

Reason: GitHub and most Markdown tools draw a Mermaid block without a plug-in. The source stays
text, so a diff shows each change. Styles make the diagram unclear in dark and high contrast
modes.

Test: `scripts/check_specs.py` checks the block, its first line and the styles.
