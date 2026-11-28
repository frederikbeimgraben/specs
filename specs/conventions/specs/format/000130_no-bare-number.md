---
id: "000130"
title: A Markdown file has no rule number outside a reference
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
  - spezi.toml
scope:
  - specs/
---

# A Markdown file has no rule number outside a reference

In a Markdown file, a rule number must not stand outside `(spec ...)`. These parts are the only
exceptions: the front matter, the tables that `spezi` writes, and text in backticks or in a code
block.

Reason: Each rule number is then a reference that the check can examine (spec 000017).

Test: `spezi check`: no Markdown file has a rule number outside `(spec ...)`, outside the
exceptions.
