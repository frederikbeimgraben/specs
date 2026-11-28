---
id: "000090"
title: The CI migrates demo projects from each migration
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

# The CI migrates demo projects from each migration

The kit must have a CI workflow that runs on each pull request and on each push to `main`. For
each start commit (spec 000203), the workflow must migrate two demo projects:

| Demo | Before the migration |
| --- | --- |
| `kit` | The kit at the start commit, with the kit at the start commit as an upstream entry in `spezi.toml`. |
| `init` | An empty git repository in which the program of the start commit ran `spezi init`. |

Reason: A change of the kit can break a migration that ran before.

Test: `.github/workflows/migrations.yml`.
