---
id: "000271"
title: The block starts and ends with a marker line
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

# The block starts and ends with a marker line

The block in `AGENTS.md` (spec 000079) must start with the line
`<!-- spezi:begin (written by spezi install, do not edit) -->`. It must end with the line
`<!-- spezi:end -->`.

Reason: The command finds the block again, and a person sees that the command writes it.

Test: `tests/test_settings.py`.
