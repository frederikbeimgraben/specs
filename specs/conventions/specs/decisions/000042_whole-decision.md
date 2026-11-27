---
id: "000042"
title: A decision spec records one decision with its alternatives
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - src/specs_kit/check.py
  - src/specs_kit/sections.py
  - .specs/templates/TEMPLATE-decision.md
scope:
  - specs/
---

# A decision spec records one decision with its alternatives

A decision spec must record one design decision. The rule text must state the decision with
`must` or `must not`.

The body must have the `#` title, the rule text and then exactly these `##` sections, in this
order:

| Section | Content |
| --- | --- |
| `## Context` | The problem and the limits that caused the decision. |
| `## Decision` | The solution that the product uses. |
| `## Alternatives` | Each solution that the owner did not choose, with the cause. |
| `## Consequences` | What becomes easier and what becomes more difficult. |

The labels `Reason:` and `Test:` come after the last section.

Reason: An agent finds the alternatives that the owner did not choose. It does not propose them
again.

Test: `specs check` checks the headings and their order.
