---
id: "000033"
title: A structure spec shows one structure as one diagram
kind: convention
status: draft
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - scripts/check_specs.py
  - specs/TEMPLATE-structure.md
scope:
  - specs/
---

# A structure spec shows one structure as one diagram

A structure spec must show one structure of the product as one UML diagram: for example the
classes of one module, the states of one life cycle or the messages of one sequence. It must
not show two structures. One structure must not spread over several specs.

The body must have the `#` title, the rule text and then exactly these `##` sections, in this
order:

| Section | Content |
| --- | --- |
| `## Diagram` | One Mermaid code block (000034). |
| `## Elements` | One table with one row for each element of the diagram (000035). |

The labels `Reason:` and `Test:` come after the last section. The rule text must say which
property of the code must agree with the diagram.

Reason: The rule ID then points to one diagram. The reader sees the structure and the rule
that binds it in one file.

Test: `scripts/check_specs.py` checks the headings and their order.
