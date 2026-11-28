---
id: "000120"
title: A spec uses no other headings
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

# A spec uses no other headings

A spec must not use a heading other than its `#` title and the `##` sections of its kind. Only
these kinds have sections: protocol (spec 000027), structure (spec 000033) and decision
(spec 000042).

Reason: A heading divides a spec into parts, and one rule has no free parts.

Test: `spezi check`: the body has only the allowed sections.
