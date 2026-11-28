---
id: "000248"
title: A rule object has six keys
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/data.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# A rule object has six keys

A rule object of the JSON output (spec 000080) must hold `kind` (the kind letter), `id` (the short
form (spec 000047)), `long` (the long form), `status`, `title` and `path`.

Reason: A script finds each part of a rule without parsing.

Test: `tests/test_json.py`.
