---
id: "000070"
title: spezi resolve prints the long form of an ID
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
tests:
  - tests/test_queries.py:test_resolve_prints_the_long_form
  - tests/test_queries.py:test_resolve_stops_for_an_unknown_id
implementation:
  - src/spezi/queries.py
  - src/spezi/project.py
scope:
  - src/spezi/
---

# spezi resolve prints the long form of an ID

`spezi resolve <id>` must print the long form (spec 000047) for a short or a long form, for
example `C/specs/format/000012` for `000012`. It must stop with an error when no rule of the
project or of a copy has this ID.

Reason: An agent gets the kind and the place of a rule without a search.

Test: `tests/test_queries.py`.
