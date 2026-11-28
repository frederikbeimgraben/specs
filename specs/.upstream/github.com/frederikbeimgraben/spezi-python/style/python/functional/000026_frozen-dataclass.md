---
id: "000026"
title: A Python data type is a frozen dataclass with slots
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# A Python data type is a frozen dataclass with slots

A Python data type must be a `@dataclass(frozen=True, slots=True)` (spec github.com/frederikbeimgraben/spezi-functional:000007).

Reason: `frozen=True` stops each change of a field, and `slots=True` stops a new field.

Test: A review.
