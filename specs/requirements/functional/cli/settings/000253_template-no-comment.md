---
id: "000253"
title: The template of spezi.toml has no comment
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_settings.py:test_init_writes_the_settings_without_comments
implementation:
  - src/spezi/data/spezi.toml
scope:
  - src/spezi/
  - spezi.toml
---

# The template of spezi.toml has no comment

The template `src/spezi/data/spezi.toml` must hold each key with its default and no comment.

Reason: The table of the settings (spec 000078) explains each key. A comment in each project
gets old.

Test: `tests/test_settings.py`.
