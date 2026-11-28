---
id: "000273"
title: The text around the block stays
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_settings.py:test_the_block_keeps_the_text_around_it
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

# The text around the block stays

`spezi install` must not change the text before and after the block in `AGENTS.md`
(spec 000079).

Reason: A person writes the other rules for agents in the same file.

Test: `tests/test_settings.py`.
