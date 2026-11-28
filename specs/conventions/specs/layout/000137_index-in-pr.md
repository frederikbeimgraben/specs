---
id: "000137"
title: A pull request with a new rule updates the index
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
  - src/spezi/index.py
scope:
  - specs/
---

# A pull request with a new rule updates the index

A pull request that adds, moves or removes a rule must update the index with `spezi install`.

Reason: A review sees each new rule in the diff of the index.

Test: `spezi check` fails when `specs/README.md` is not current.
