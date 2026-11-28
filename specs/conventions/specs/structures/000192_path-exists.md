---
id: "000192"
title: The path of an element exists
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

# The path of an element exists

The path of an element (spec 000036) must exist.

Reason: A moved file breaks the check, so the diagram cannot point to old code.

Test: `spezi check` checks that each path exists.
