---
id: "000075"
title: ruff format changes nothing
kind: style
status: draft
owner: frederikbeimgraben
updated: 2026-11-27
implementation:
  - pyproject.toml
scope:
  - src/
  - pyproject.toml
---

# ruff format changes nothing

`ruff format --check` must report no file to change, with the settings in `pyproject.toml`.

Reason: One fixed format keeps the diffs of people and agents small.

Test: `ruff format --check`.
