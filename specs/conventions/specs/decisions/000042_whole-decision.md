---
id: "000042"
title: A decision spec has fixed sections
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
  - src/spezi/sections.py
  - specs/.templates/TEMPLATE-decision.md
scope:
  - specs/
---

# A decision spec has fixed sections

The body of a decision spec must have the `#` title, the rule text and then exactly these `##`
sections, in this order:

| Section | Content |
| --- | --- |
| `## Context` | The problem and the limits that caused the decision. |
| `## Decision` | The solution that the product uses. |
| `## Alternatives` | Each solution that the owner did not choose, with the cause. |
| `## Consequences` | What becomes easier and what becomes more difficult. |

Reason: An agent finds the alternatives that the owner did not choose. It does not propose them
again.

Test: `spezi check` checks the headings and their order.
