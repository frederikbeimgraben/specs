---
id: "000324"
title: The language server checks at three times
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_lsp.py:test_the_server_checks_the_text_while_it_changes
implementation:
  - src/spezi/lsp.py
  - src/spezi/check.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# The language server checks at three times

The language server (spec 000088) must check the project at these times:

1. When the client starts it: the whole project, from the files on the disk.
2. 300 ms after the last change of an open file: only this file, with the text in the editor.
3. When the client saves a file: the whole project, from the files on the disk. The server
   removes each diagnostic of a file that has no error and no warning now.

Reason: A person sees an error while typing. A full check runs only when the files change on
the disk.

Test: `tests/test_lsp.py`.
