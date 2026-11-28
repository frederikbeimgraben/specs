---
id: "000275"
title: spezi init writes CLAUDE.md
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_settings.py:test_init_writes_agents_and_claude
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

# spezi init writes CLAUDE.md

`spezi init` must create `CLAUDE.md` with the line `@AGENTS.md` when the file does not exist.

Reason: Claude Code reads `AGENTS.md` through the import in `CLAUDE.md`.

Test: `tests/test_settings.py`.
