---
id: "000326"
title: The hover shows the rule
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_lsp.py:test_the_hover_shows_the_rule
implementation:
  - src/spezi/lsp.py
  - src/spezi/check.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# The hover shows the rule

On a reference (spec 000325), the language server must give a hover. The hover shows
the long form, the title, the status and the text of the rule after the front matter.

Reason: The editor shows the text of a rule without a change of file.

Test: `tests/test_lsp.py`.
