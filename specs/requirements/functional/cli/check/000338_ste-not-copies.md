---
id: "000338"
title: The check of ASD-STE100 skips the copies
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/ste.py
  - src/spezi/check.py
  - src/spezi/data/ste/
scope:
  - src/spezi/
---

# The check of ASD-STE100 skips the copies

`spezi check` must not check the rules of the copies against ASD-STE100 (spec 000093).

Reason: The project cannot change the text of a copy (spec 000048).

Test: Review.
