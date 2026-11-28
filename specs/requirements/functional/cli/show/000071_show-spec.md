---
id: "000071"
title: spezi show prints the full text of a spec
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
tests:
  - tests/test_queries.py:test_show_prints_the_full_text
  - tests/test_queries.py:test_show_stops_for_an_unknown_id
implementation:
  - src/spezi/queries.py
scope:
  - src/spezi/
---

# spezi show prints the full text of a spec

`spezi show <id>` must print the full text of the spec file for a short or a long form of
000047. It must stop with an error when no rule of the project or of a copy has this ID.

Reason: An agent reads a rule of a copy with the same command as a rule of the project.

Test: `tests/test_queries.py`.
