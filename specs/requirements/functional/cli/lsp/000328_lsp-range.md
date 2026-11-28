---
id: "000328"
title: The hover marks only the rule ID
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_lsp.py:test_the_link_marks_the_reference_in_the_code
implementation:
  - src/spezi/lsp.py
  - src/spezi/check.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# The hover marks only the rule ID

The hover and the definition (spec 000326, 000327) must mark only the rule ID
of the item, for example `000089` in `(spec 000088, 000089)`. They must not mark `(spec `, the
parentheses or the whole line.

Reason: Each ID of a list gets its own hover.

Test: `tests/test_lsp.py`.
