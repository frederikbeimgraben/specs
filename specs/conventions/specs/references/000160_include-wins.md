---
id: "000160"
title: include wins over own
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_kit.py:test_add_copies_an_own_folder_that_include_names
implementation:
  - src/spezi/changes.py
  - src/spezi/check.py
  - src/spezi/kit.py
  - src/spezi/install.py
scope:
  - specs/
---

# include wins over own

A folder of `own` (spec 000159) that `include` names, or that holds a folder of
`include`, must be in the copy.

Reason: A project that names a folder in `include` wants its rules.

Test: `tests/test_kit.py`.
