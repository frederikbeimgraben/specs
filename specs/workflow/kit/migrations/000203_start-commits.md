---
id: "000203"
title: The start commits come from the migrations
kind: workflow
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - .github/workflows/migrations.yml
  - .github/scripts/migration-demo.sh
  - .github/scripts/migration_starts.py
scope:
  - src/spezi/migrations/
  - .github/
---

# The start commits come from the migrations

The migration workflow (spec 000090) must get its start commits from `src/spezi/migrations/`
(spec 000081). For each commit that changed a migration, the start commit is the parent of that
commit. Each start commit occurs one time.

Reason: Each project state before a migration is then a demo.

Test: `.github/scripts/migration_starts.py`.
