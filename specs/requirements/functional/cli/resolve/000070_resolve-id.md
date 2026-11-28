---
id: "000070"
title: spezi resolve prints the long form of an ID
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_queries.py:test_resolve_prints_the_long_form
implementation:
  - src/spezi/queries.py
  - src/spezi/project.py
scope:
  - src/spezi/
---

# spezi resolve prints the long form of an ID

`spezi resolve <id>` must print the long form (spec 000047) for a short or a long form, for
example `C/specs/format/000012` for `000012`.

Reason: An agent gets the kind and the place of a rule without a search.

Test: `tests/test_queries.py`.
