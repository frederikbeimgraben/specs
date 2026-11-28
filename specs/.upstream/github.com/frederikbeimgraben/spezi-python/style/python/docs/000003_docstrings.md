---
id: "000003"
title: Each module, class and function has a docstring
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# Each module, class and function has a docstring

Each module, class and function must have a docstring.

Reason: Tools show the docstring to the reader of the code.

Test: The ruff rules `D100` to `D107` find a public name without a docstring (spec 000028). A
review finds a private name without a docstring.
