---
id: "000220"
title: spezi new gives the next free number
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_new.py:test_new_skips_the_numbers_of_the_copies
implementation:
  - src/spezi/new.py
scope:
  - src/spezi/
---

# spezi new gives the next free number

`spezi new` must give the new spec the highest number of `specs/` and of `base_ref` plus one
(spec 000013).

Reason: Two branches then get different numbers in most cases (spec 000122).

Test: `tests/test_new.py`.
