---
id: "000254"
title: A migration removes the comments of an old template
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_migrations.py:test_migration_6_removes_the_comments_of_the_template
implementation:
  - src/spezi/migrations/
scope:
  - src/spezi/
  - spezi.toml
---

# A migration removes the comments of an old template

A migration (spec 000081) must remove each line of `spezi.toml` that is a comment of an earlier
template. A different comment must stay.

Reason: The comments of the old template get old. The comments of a person stay.

Test: `tests/test_migrations.py`.
