---
id: "000090"
title: The CI migrates demo projects from each migration
kind: workflow
status: draft
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - .github/workflows/migrations.yml
  - .github/scripts/migration-demo.sh
  - .github/scripts/migration_starts.py
scope:
  - src/specs_kit/migrations/
  - .github/
---

# The CI migrates demo projects from each migration

The kit must have a CI workflow that runs on each pull request and on each push to `main`. The
workflow must get its start commits from `src/specs_kit/migrations/` (000081): for each commit
of a migration, the parent of that commit, one time for each commit. For each start commit, the
workflow must migrate two demo projects:

| Demo | Before the migration |
| --- | --- |
| `kit` | The kit at the start commit, with the kit at the start commit as an upstream entry in `specs.toml`. |
| `init` | An empty git repository in which the program of the start commit ran `specs init`. |

The workflow must then run `specs install` of the program of the pull request in the demo
project two times. The run is correct only when the first `specs install` shows 0 errors and
the second `specs install` changes no file.

Reason: A change of the kit can break a migration that ran before. The second `specs install`
shows a migration that changes a file again.

Test: `.github/workflows/migrations.yml`.
