---
id: "000002"
title: basedpyright reports no error
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# basedpyright reports no error

basedpyright must report 0 errors with the settings in `pyproject.toml`.

Reason: The type checker finds an error before a test or a user does.

Test: `basedpyright`.
