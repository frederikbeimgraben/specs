---
id: "000222"
title: spezi new needs a scope that exists
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_new.py:test_new_stops_for_a_missing_scope_path
  - tests/test_new.py:test_new_needs_a_scope
implementation:
  - src/spezi/new.py
scope:
  - src/spezi/
---

# spezi new needs a scope that exists

`spezi new` must get one `--scope` for each path. Each path must exist. Without a scope, or when a
scope path does not exist, the command must stop with an error and write no file.

Reason: Each spec controls a part of the project that exists (spec 000009).

Test: `tests/test_new.py`.
