---
id: "000187"
title: The first line of the diagram names its type
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

# The first line of the diagram names its type

The first line of the Mermaid block (spec 000034) must name the diagram type of the key
`diagram`:

| `diagram` | First line | Use |
| --- | --- | --- |
| `class` | `classDiagram` | Classes, models and their relations. |
| `state` | `stateDiagram-v2` | The states and the transitions of one life cycle. |
| `sequence` | `sequenceDiagram` | The messages between parts, in time order. |
| `entity` | `erDiagram` | Tables, their columns and their relations. |
| `component` | `flowchart` | Components, services and their connections. |

Reason: The key tells a tool the type without a parser for Mermaid.

Test: `spezi check` checks the first line.
