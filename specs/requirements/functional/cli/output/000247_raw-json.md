---
id: "000247"
title: --json and --raw do not go together
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_json.py:test_raw_and_json_exclude_each_other
implementation:
  - src/spezi/data.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# --json and --raw do not go together

A command with both `--json` and `--raw` (spec 000238) must stop with an error.

Reason: The two options ask for two different outputs.

Test: `tests/test_json.py`.
