---
id: "000041"
title: The status of a spec moves from draft to approved, replaced or removed
kind: structure
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
diagram: state
implementation:
  - specs/.templates/TEMPLATE.md
  - specs/conventions/specs/format/000010_status.md
scope:
  - specs/
---

# The status of a spec moves from draft to approved, replaced or removed

The status of a spec must change only along an arrow of this diagram.

## Diagram

```mermaid
stateDiagram-v2
  [*] --> draft : copy the template
  draft --> approved : the owner approves
  approved --> draft : the rule changes
  draft --> removed : the owner drops it
  approved --> replaced : a new rule replaces it
  approved --> removed : the rule is not in force
  replaced --> [*]
  removed --> [*]
```

## Elements

| Element | Path | Meaning |
| --- | --- | --- |
| `draft` | specs/.templates/TEMPLATE.md | The owner did not approve the spec yet. |
| `approved` | specs/conventions/specs/format/000010_status.md | The owner approved the spec. |
| `replaced` | specs/conventions/specs/format/000010_status.md | A different spec replaces the spec and names it in `replaces`. `replaced_by` names that spec. |
| `removed` | specs/conventions/specs/format/000010_status.md | The spec is not in force. The number stays taken. |

Reason: Each arrow is one step that the owner can examine.

Test: Review.
