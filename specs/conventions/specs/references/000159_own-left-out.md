---
id: "000159"
title: A copy leaves out the own folders of its repository
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_kit.py:test_init_leaves_out_the_own_folders_of_the_kit
implementation:
  - src/spezi/changes.py
  - src/spezi/check.py
  - src/spezi/kit.py
  - src/spezi/install.py
scope:
  - specs/
---

# A copy leaves out the own folders of its repository

When the `spezi.toml` of the repository has `own` (spec 000078), the copy (spec 000048) must not
hold the folders below `specs/` that `own` names. An example is `own = ["requirements/"]`.

Reason: These folders hold the rules that apply only to the repository itself.

Test: `tests/test_kit.py`.
