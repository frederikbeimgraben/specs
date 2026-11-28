---
id: "000278"
title: A migration changes only the old format
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_migrations.py:test_a_migration_changes_nothing_twice
implementation:
  - src/spezi/migrations/
  - src/spezi/kit.py
  - src/spezi/cli.py
  - src/spezi/install.py
scope:
  - src/spezi/
---

# A migration changes only the old format

A migration (spec 000081) must change only what it finds in the old format.

Reason: A second run then changes nothing.

Test: `tests/test_migrations.py`.
