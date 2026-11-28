---
id: "000279"
title: A command runs each migration that a ref does not hold
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_migrations.py:test_update_of_the_kit_runs_no_migration_that_the_kit_holds
implementation:
  - src/spezi/migrations/
  - src/spezi/kit.py
  - src/spezi/cli.py
  - src/spezi/install.py
scope:
  - src/spezi/
---

# A command runs each migration that a ref does not hold

A kit ref holds a migration (spec 000081) when its commit is the commit of the migration or a
later commit on the same history (`git merge-base --is-ancestor`). `spezi update`, `spezi add`
and `spezi install` must run each migration that a ref does not hold, oldest first, before they
copy:

| Target | Ref |
| --- | --- |
| The project and each copy, on an update of the kit | The kit commit in `spezi.lock` of the project before the update, else the kit ref in its `spezi.toml`. |
| The project, on `spezi install` | The same ref. Without a kit entry, no migration runs. |
| The new copy of the kit | The commit of the copy. |
| The copy of a different repository | The kit commit in `spezi.lock` of that repository at its commit, else the kit ref in its `spezi.toml`. Without one, each migration runs. |

Reason: Each project and each copy gets each migration one time.

Test: `tests/test_migrations.py`.
