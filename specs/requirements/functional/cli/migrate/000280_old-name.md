---
id: "000280"
title: The command reads the files of the old name
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_migrations.py:test_migration_5_gives_the_files_the_new_name
implementation:
  - src/spezi/migrations/
  - src/spezi/kit.py
  - src/spezi/cli.py
  - src/spezi/install.py
scope:
  - src/spezi/
---

# The command reads the files of the old name

Until a migration gives them the new names, a command must read `specs.toml`, `specs.lock` and
the name `github.com/frederikbeimgraben/specs` as those of the kit.

Reason: The kit had the name `specs` before. A project of that time can still update.

Test: `tests/test_migrations.py`.
