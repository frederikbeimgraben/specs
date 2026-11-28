---
id: "000049"
title: Each rule of a different repository applies unless a project rule replaces it
kind: convention
status: draft
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# Each rule of a different repository applies unless a project rule replaces it

Each rule of a copy (spec 000048) with the status `draft` or `approved` must apply to the
project.

Reason: A new rule of the different repository applies after the next update.

Test: Review.
