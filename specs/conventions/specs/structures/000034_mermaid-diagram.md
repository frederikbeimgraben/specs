---
id: "000034"
title: The diagram is one Mermaid block of a fixed type
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

# The diagram is one Mermaid block of a fixed type

`## Diagram` must hold exactly one fenced code block with the language `mermaid`.

Reason: GitHub and most Markdown tools draw a Mermaid block without a plug-in. The source stays
text, so a diff shows each change.

Test: `spezi check` checks the block.
