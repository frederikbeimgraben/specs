---
id: "000261"
title: With agents off, spezi check skips the block
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
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

# With agents off, spezi check skips the block

When the switch `agents` is off (spec 000084), `spezi check` must not check the block in
`AGENTS.md`.

Reason: Without the part, the project has no block.

Test: Review.
