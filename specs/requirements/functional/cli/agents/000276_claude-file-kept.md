---
id: "000276"
title: spezi init keeps a CLAUDE.md without the import
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_settings.py:test_init_keeps_an_existing_claude
implementation:
  - src/spezi/agents.py
  - src/spezi/check.py
  - src/spezi/cli.py
  - src/spezi/migrations/m0003_agents_marker.py
scope:
  - src/spezi/
  - AGENTS.md
  - CLAUDE.md
---

# spezi init keeps a CLAUDE.md without the import

When `CLAUDE.md` exists without the line `@AGENTS.md`, `spezi init` must not change it. It must
print the line to add.

Reason: The file belongs to the person.

Test: `tests/test_settings.py`.
