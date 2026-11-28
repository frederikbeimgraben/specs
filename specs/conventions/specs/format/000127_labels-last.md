---
id: "000127"
title: The labels come after the rule text and the sections
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# The labels come after the rule text and the sections

The rule text and the `##` sections of the kind must come before the labels (spec 000015).

Reason: A reader finds the rule first, and the cause and the test at the end.

Test: `spezi check`.
