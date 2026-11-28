---
id: "000162"
title: A copy of an older kit holds the migrated rules
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/changes.py
  - src/spezi/check.py
  - src/spezi/kit.py
  - src/spezi/install.py
scope:
  - specs/
---

# A copy of an older kit holds the migrated rules

When the repository uses an older kit, the copy (spec 000048) must hold its rules after the
migrations (spec 000081). Else the copy must hold the rules with no change.

Reason: The check of the project reads every rule in the current format.

Test: `tests/test_migrations.py`.
