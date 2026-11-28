---
id: "000110"
title: spezi new makes the copy of the template
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/
scope:
  - specs/
---

# spezi new makes the copy of the template

A person or an agent must make the copy of the template (spec 000008) with
`spezi new <kind> <area>/<topic> <name> "<title>" --scope <path>` (spec 000069).

Reason: The command gives the next free number (spec 000013), so that nobody must count by hand.

Test: Review.
