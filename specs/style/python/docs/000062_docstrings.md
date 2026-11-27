---
id: "000062"
title: Python code is documented in Google-style docstrings
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
implementation:
  - pyproject.toml
  - src/specs_kit/
scope:
  - src/
  - pyproject.toml
---

# Python code is documented in Google-style docstrings

Every module, class and function must have a docstring in the Google format. A function body
must not hold a `#` comment. A reason or a note must go into the docstring.

Reason: One place for the documentation. Tools show a docstring, but not a comment in the body.

Test: ruff rule set `D` with the Google convention. A review finds a comment in a body.
