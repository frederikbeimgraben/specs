---
id: "000006"
title: ruff format changes nothing
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# ruff format changes nothing

`ruff format --check` must report no file to change, with the settings in `pyproject.toml`.

Reason: One fixed format keeps the diffs of people and agents small.

Test: `ruff format --check`.
