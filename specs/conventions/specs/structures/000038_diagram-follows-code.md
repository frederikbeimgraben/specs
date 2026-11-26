---
id: "000038"
title: A change of the structure changes the diagram
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - specs/
scope:
  - specs/
---

# A change of the structure changes the diagram

A change of the code that adds, removes or renames an element of a structure spec, or a relation
between two elements, must change the diagram in the same pull request. A diagram must show the
code as it is, not a plan. A planned structure must be a structure spec with `status: draft`
and `implementation: null`.

Reason: A diagram that does not show the code is wrong after the next change, and nobody sees
it.

Test: Review. `scripts/check_specs.py` finds an element path that does not exist.
