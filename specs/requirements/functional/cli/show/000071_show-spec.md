---
id: "000071"
title: spezi show prints the full text of a spec
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_queries.py:test_show_prints_the_full_text
implementation:
  - src/spezi/queries.py
scope:
  - src/spezi/
---

# spezi show prints the full text of a spec

`spezi show <id>` must print the full text of the spec file for the short or the long form of
its ID (spec 000047).

Reason: An agent reads a rule of a copy with the same command as a rule of the project.

Test: `tests/test_queries.py`.
