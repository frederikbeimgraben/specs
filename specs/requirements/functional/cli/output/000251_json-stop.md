---
id: "000251"
title: A stop with --json gives an error object
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_json.py:test_a_stop_gives_an_error_object
implementation:
  - src/spezi/data.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# A stop with --json gives an error object

When a command with `--json` stops with an error, also for a wrong argument, it must print
`{"error": "<error>"}` to stdout and nothing to stderr. It must end with the exit code 1.

Reason: A script reads stdout only and still gets the error.

Test: `tests/test_json.py`.
