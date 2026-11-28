---
id: "000329"
title: The language server writes no file
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_lsp.py:test_the_server_writes_no_file
implementation:
  - src/spezi/lsp.py
  - src/spezi/check.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# The language server writes no file

The language server (spec 000088) must not write a file.

Reason: The editor owns the files that it shows.

Test: `tests/test_lsp.py`.
