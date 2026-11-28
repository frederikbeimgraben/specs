---
id: "000262"
title: claude needs agents
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_features.py:test_claude_needs_agents
implementation:
  - src/spezi/project.py
  - src/spezi/install.py
  - src/spezi/kit.py
  - src/spezi/devshell.py
  - src/spezi/check.py
  - src/spezi/data/spezi.toml
scope:
  - src/spezi/
  - spezi.toml
---

# claude needs agents

`claude = true` with `agents = false` must be an error of `spezi.toml` (spec 000255).

Reason: `CLAUDE.md` only imports `AGENTS.md`.

Test: `tests/test_features.py`.
