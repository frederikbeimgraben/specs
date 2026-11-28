---
id: "000204"
title: A migrated demo installs two times
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

# A migrated demo installs two times

The migration workflow (spec 000090) must run `spezi install` of the program of the pull request
two times in each demo project. The run is correct only when the first `spezi install` shows 0
errors and the second `spezi install` changes no file.

Reason: The second `spezi install` shows a migration that changes a file again.

Test: `.github/scripts/migration-demo.sh`.
