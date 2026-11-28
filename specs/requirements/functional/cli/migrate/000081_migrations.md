---
id: "000081"
title: spezi migrates a project and its copies to a new kit
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_migrations.py:test_update_moves_the_old_layout
  - tests/test_migrations.py:test_a_migration_changes_nothing_twice
  - tests/test_migrations.py:test_add_stops_for_a_newer_kit
  - tests/test_migrations.py:test_migration_5_gives_the_files_the_new_name
implementation:
  - src/spezi/migrations/
  - src/spezi/kit.py
  - src/spezi/cli.py
  - src/spezi/install.py
scope:
  - src/spezi/
---

# spezi migrates a project and its copies to a new kit

A change of the kit that changes a file place, a file format or `spezi.toml` must come with a
migration: a Python function in `src/spezi/migrations/` that names the commit of the kit
with the change. A migration must change only what it finds in the old format, so that a
second run changes nothing.

A kit ref holds a migration when its commit is the commit of the migration or a later commit
on the same history (`git merge-base --is-ancestor`). `spezi update`, `spezi add` and
`spezi install` must run each migration that a ref does not hold, oldest first, before they
copy:

| Target | Ref |
| --- | --- |
| The project and each copy, on an update of the kit | The kit commit in `spezi.lock` of the project before the update, else the kit ref in its `spezi.toml`. |
| The project, on `spezi install` | The same ref. Without a kit entry, no migration runs. |
| The copy of a different repository | The kit commit in `spezi.lock` of that repository at its commit, else the kit ref in its `spezi.toml`. Without one, each migration runs. |

The kit had the name `specs` before. A project or a repository from that time has `specs.toml`
and `specs.lock`, and names the kit `github.com/frederikbeimgraben/specs`. Until a migration gives
them the new names, the command must read these files and this name as the files and the name
of the kit.

When a different repository needs a kit that the kit ref of the project does not hold, the
command must stop with an error that tells to run `spezi update` first, and change no file.
The command must print one line `migrated: <description>` for each migration that ran, and
list the changed files (000077).

Reason: A new kit can change the format without manual work in each project, and the copies of
older repositories stay readable.

Test: `tests/test_migrations.py`.
