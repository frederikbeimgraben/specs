---
id: "000126"
title: A label starts its own paragraph
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# A label starts its own paragraph

Each label (spec 000015) must be at the start of its own paragraph.

Reason: A tool finds a label only at the start of a paragraph.

Test: `spezi check`.
