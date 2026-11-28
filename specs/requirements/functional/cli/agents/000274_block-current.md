---
id: "000274"
title: spezi check finds a block that is not current
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
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

# spezi check finds a block that is not current

`spezi check` must show an error when the block in `AGENTS.md` (spec 000079) is not current.

Reason: The file stays current with the specs.

Test: `tests/test_settings.py`.
