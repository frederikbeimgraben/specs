---
id: "000027"
title: A collection field has the type tuple, frozenset or Mapping
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# A collection field has the type tuple, frozenset or Mapping

A collection field of a data type must have the type `tuple`, `frozenset` or `Mapping`
(spec github.com/frederikbeimgraben/spezi-functional:000014).

Reason: These types have no methods that change the collection.

Test: A review.
