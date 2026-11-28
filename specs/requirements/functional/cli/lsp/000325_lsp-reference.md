---
id: "000325"
title: A reference in the editor is a rule ID or a spec reference
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/lsp.py
  - src/spezi/check.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# A reference in the editor is a rule ID or a spec reference

For the language server (spec 000088), a reference in a front matter must be a rule ID in
short or long form (spec 000047). In each other text, a reference must be an item
of a `(spec ...)` reference (spec 000017).

Reason: The hover and the definition (spec 000326, 000327) find the same references as the check.

Test: `tests/test_lsp.py`.
