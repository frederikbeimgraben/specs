---
id: "000073"
title: specs search finds rules by a text
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
tests:
  - tests/test_queries.py:test_search_ignores_the_case
implementation:
  - src/specs_kit/queries.py
scope:
  - src/specs_kit/
---

# specs search finds rules by a text

`specs search <text>` must print the lines of `specs list` for each rule whose title or body
holds `<text>`. Upper and lower case must not change the result.

Reason: An agent finds the rules of a topic without a search by hand.

Test: `tests/test_queries.py`.
