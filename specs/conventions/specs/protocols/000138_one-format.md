---
id: "000138"
title: A protocol spec describes one format
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/
scope:
  - specs/
---

# A protocol spec describes one format

A protocol spec must describe exactly one data exchange format: one message, one payload, one
file or one export. Two formats must not share one spec.

Reason: The rule ID then points to one format.

Test: Review.
