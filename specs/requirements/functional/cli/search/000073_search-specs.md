---
id: "000073"
title: spezi search finds rules by a text
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/queries.py
scope:
  - src/spezi/
---

# spezi search finds rules by a text

`spezi search <text>` must print the lines of `spezi list` for each rule whose title or body
holds `<text>`.

Reason: An agent finds the rules of a topic without a search by hand.

Test: `tests/test_queries.py`.
