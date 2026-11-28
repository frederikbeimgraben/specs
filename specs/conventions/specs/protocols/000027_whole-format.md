---
id: "000027"
title: A protocol spec has fixed sections
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
  - src/spezi/sections.py
  - specs/.templates/TEMPLATE-protocol.md
scope:
  - specs/
---

# A protocol spec has fixed sections

The body of a protocol spec must have the `#` title, the rule text and then exactly these `##`
sections, in this order:

| Section | Content |
| --- | --- |
| `## Transport` | The medium, the direction, the address, the headers and the authentication. |
| `## Schema` | The name of the schema file, or a table for a format that is not JSON (spec 000028). |
| `## Example` | At least one complete example in a code block (spec 000029). |
| `## Compatibility` | What a receiver must accept, so that a compatible change does not break it (spec 000030). |

Reason: One file holds the full contract.

Test: `spezi check` checks the headings and their order.
