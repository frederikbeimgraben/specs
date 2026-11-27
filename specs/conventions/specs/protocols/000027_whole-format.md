---
id: "000027"
title: A protocol spec describes one whole format
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - src/specs_kit/check.py
  - .specs/templates/TEMPLATE-protocol.md
scope:
  - specs/
---

# A protocol spec describes one whole format

A protocol spec must describe one data exchange format as a whole: one message, one payload,
one file or one export. One format must not spread over several specs. Two formats must not
share one spec.

The body must have the `#` title, the rule text and then exactly these `##` sections, in this
order:

| Section | Content |
| --- | --- |
| `## Transport` | The medium, the direction, the address, the headers and the authentication. |
| `## Schema` | The name of the schema file, or a table for a format that is not JSON (000028). |
| `## Example` | At least one complete example in a code block (000029). |
| `## Compatibility` | What a receiver must accept, so that a compatible change does not break it (000030). |

The labels `Reason:` and `Test:` come after the last section.

Reason: A receiver builds against a format as a whole. One file then holds the full contract.

Test: `specs check` checks the headings and their order.
