---
id: "000081"
title: spezi migrates a project and its copies to a new kit
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_migrations.py:test_update_moves_the_old_layout
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
migration. A migration is a Python function in `src/spezi/migrations/` that names the commit of
the kit with the change.

Reason: A new kit can change the format without manual work in each project.

Test: `tests/test_migrations.py`.
