---
id: "000282"
title: Each migration that ran gives one line
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/migrations/
  - src/spezi/kit.py
  - src/spezi/cli.py
  - src/spezi/install.py
scope:
  - src/spezi/
---

# Each migration that ran gives one line

The command must print one line `migrated: <description>` for each migration (spec 000081) that
ran.

Reason: The person sees why files changed.

Test: `tests/test_migrations.py`.
