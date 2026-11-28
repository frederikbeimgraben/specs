---
id: "000298"
title: spezi update of the kit replaces the kit files
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/kit.py
  - src/spezi/cli.py
  - src/spezi/devshell.py
scope:
  - src/spezi/
---

# spezi update of the kit replaces the kit files

For the kit, `spezi update` must also replace the templates, the skills, the CI files
(spec 000066) and the entry `spezi` in `.mcp.json`. A template or a skill that the user keeps
(spec 000085) stays.

Reason: The project gets the new templates and skills with the new rules.

Test: `tests/test_questions.py`.
