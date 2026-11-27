---
id: "000081"
title: specs migrates a project and its copies to a new kit
kind: functional
status: draft
owner: frederikbeimgraben
updated: 2026-11-27
tests:
  - tests/test_migrations.py:test_update_moves_the_old_layout
  - tests/test_migrations.py:test_a_migration_changes_nothing_twice
  - tests/test_migrations.py:test_add_stops_for_a_newer_kit
implementation:
  - src/specs_kit/migrations/
  - src/specs_kit/kit.py
  - src/specs_kit/cli.py
  - src/specs_kit/install.py
scope:
  - src/specs_kit/
---

# specs migrates a project and its copies to a new kit

A change of the kit that changes a file place, a file format or `specs.toml` must come with a
migration: a Python function in `src/specs_kit/migrations/` that names the commit of the kit
with the change. A migration must change only what it finds in the old format, so that a
second run changes nothing.

A kit ref holds a migration when its commit is the commit of the migration or a later commit
on the same history (`git merge-base --is-ancestor`). `specs update`, `specs add` and
`specs install` must run each migration that a ref does not hold, oldest first, before they
copy:

| Target | Ref |
| --- | --- |
| The project and each copy, on an update of the kit | The kit commit in `specs.lock` of the project before the update, else the kit ref in its `specs.toml`. |
| The project, on `specs install` | The same ref. Without a kit entry, no migration runs. |
| The copy of a different repository | The kit commit in `specs.lock` of that repository at its commit, else the kit ref in its `specs.toml`. Without one, each migration runs. |

When a different repository needs a kit that the kit ref of the project does not hold, the
command must stop with an error that tells to run `specs update` first, and change no file.
The command must print one line `migrated: <description>` for each migration that ran, and
list the changed files (000077).

Reason: A new kit can change the format without manual work in each project, and the copies of
older repositories stay readable.

Test: `tests/test_migrations.py`.
