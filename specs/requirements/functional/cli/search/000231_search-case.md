---
id: "000231"
title: spezi search ignores the case
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_queries.py:test_search_ignores_the_case
implementation:
  - src/spezi/queries.py
scope:
  - src/spezi/
---

# spezi search ignores the case

Upper and lower case of `<text>` must not change the result of `spezi search`.

Reason: A word at the start of a sentence has an upper case letter.

Test: `tests/test_queries.py`.
