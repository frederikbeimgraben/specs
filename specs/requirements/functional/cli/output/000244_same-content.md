---
id: "000244"
title: A write with the same content is no change
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_output.py:test_a_write_with_the_same_content_is_no_change
implementation:
  - src/spezi/changes.py
  - src/spezi/cli.py
  - src/spezi/view.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# A write with the same content is no change

A write with the same content must not go to the list of changed files (spec 000077).

Reason: A second run of a command that changes nothing shows an empty list.

Test: `tests/test_output.py`.
