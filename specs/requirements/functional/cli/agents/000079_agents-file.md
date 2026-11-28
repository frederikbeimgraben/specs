---
id: "000079"
title: spezi writes the rules for agents to AGENTS.md
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_settings.py:test_a_file_without_block_gets_it_at_the_end
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

# spezi writes the rules for agents to AGENTS.md

When the switch `agents` of `[features]` is on (spec 000084), `spezi install` must write one
block to `AGENTS.md` in the root of the project:

| State of `AGENTS.md` | `spezi install` |
| --- | --- |
| The file does not exist. | It creates the file with the block. |
| The file has no block. | It adds the block at the end. |
| The file has the block. | It replaces only the block. |

Reason: An agent finds every rule that applies in the file that it reads first.

Test: `tests/test_settings.py`.
