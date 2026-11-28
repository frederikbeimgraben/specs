---
id: "000029"
title: The rule selection of ruff is an explicit list
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# The rule selection of ruff is an explicit list

The rule selection of ruff in `pyproject.toml` must be an explicit list of rules.

Reason: An explicit list stays the same when a new ruff version changes its default rules.

Test: A review checks the selection.
