---
id: "000005"
title: ruff reports no warning
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# ruff reports no warning

`ruff check` must report 0 warnings with the rule selection in `pyproject.toml`.

Reason: Each warning of ruff is a violation of a rule (spec 000028).

Test: `ruff check`.
