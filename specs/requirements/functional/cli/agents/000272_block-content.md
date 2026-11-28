---
id: "000272"
title: The block holds the approved A and W rules
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

# The block holds the approved A and W rules

The block in `AGENTS.md` (spec 000079) must hold a short text that tells an agent how to use the
rules. Then it must hold the table of `specs/README.md` (spec 000007) with only the A and W rules
that have the status `approved`. The rules of the project come first, then the rules of the
copies (spec 000049).

Reason: An agent reads only the rules for its work.

Test: `spezi check` fails when the block in `AGENTS.md` is not current.
