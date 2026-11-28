---
id: "000181"
title: A direct table removes the conflict of two commits
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/transitive.py
  - src/spezi/kit.py
  - src/spezi/check.py
scope:
  - specs/
  - spezi.toml
---

# A direct table removes the conflict of two commits

A table for the transitive upstream in `spezi.toml` of the project must remove the error of
(spec 000180).

Reason: The table is the decision of the person, and the direct table wins
(spec 000176).

Test: Review.
