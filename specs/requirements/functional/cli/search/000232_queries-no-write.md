---
id: "000232"
title: A query writes no file
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/queries.py
scope:
  - src/spezi/
---

# A query writes no file

`spezi resolve`, `spezi show`, `spezi list` and `spezi search` must not write a file.

Reason: An agent can ask at each time without a change of the project.

Test: Review.
