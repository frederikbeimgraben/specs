---
id: "000323"
title: A finding without a line goes to line 1
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

# A finding without a line goes to line 1

In the language server (spec 000088), an error without a line must go to line 1 of its file. An
error of a folder or of a missing file must go to line 1 of `spezi.toml`, with its path in the
text.

Reason: An editor shows a diagnostic only at a line of a file.

Test: Review.
