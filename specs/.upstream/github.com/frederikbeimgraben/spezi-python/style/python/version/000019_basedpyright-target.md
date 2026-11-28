---
id: "000019"
title: The Python version of basedpyright is 3.13
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# The Python version of basedpyright is 3.13

`pythonVersion` of basedpyright in `pyproject.toml` must be `3.13`.

Reason: basedpyright then checks the code against the typing features of Python 3.13
(spec 000001).
