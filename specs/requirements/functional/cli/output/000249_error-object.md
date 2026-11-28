---
id: "000249"
title: An error object has four keys
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_json.py:test_check_gives_errors_as_objects
implementation:
  - src/spezi/data.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# An error object has four keys

An error object and a warning object of the JSON output (spec 000080) must hold four keys.
These are `file`, `line` (a whole number from 1), `message` and `rule` (the number of the named
rule). A
part that the error line does not have must be `null`.

Reason: A script reads each finding in the same way.

Test: `tests/test_json.py`.
