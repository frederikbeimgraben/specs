---
id: "000183"
title: Only init, add and update change transitive
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

# Only init, add and update change transitive

Only `spezi init`, `spezi add` and `spezi update` must change `transitive` (spec 000085).

Reason: These commands ask the user which transitive upstreams to copy.

Test: Review.
