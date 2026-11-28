---
id: "000327"
title: The definition opens the spec
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_lsp.py:test_the_definition_opens_the_spec
implementation:
  - src/spezi/lsp.py
  - src/spezi/check.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# The definition opens the spec

On a reference (spec 000325), the language server must give a definition. The
definition is the first line of the file of the rule.

Reason: The person opens the rule with one key.

Test: `tests/test_lsp.py`.
