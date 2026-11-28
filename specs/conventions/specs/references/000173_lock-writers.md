---
id: "000173"
title: Only five commands write spezi.lock
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/lock.py
  - src/spezi/check.py
  - src/spezi/kit.py
scope:
  - src/spezi/lock.py
  - spezi.toml
---

# Only five commands write spezi.lock

A command other than `spezi install`, `spezi update`, `spezi add`, `spezi init` and
`spezi remove` must not write `spezi.lock` (spec 000082, 000083, 000087).

Reason: Each of these commands changes or loads a copy, and the lock must agree with the copies.

Test: Review.
