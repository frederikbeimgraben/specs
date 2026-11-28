---
id: "000088"
title: spezi lsp runs the language server
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

# spezi lsp runs the language server

`spezi lsp` must run a language server on stdin and stdout. The server uses the root of the
workspace as the root of the project. It serves the specs below `specs/`, each other Markdown
file that git tracks, and the files of `code_dirs` with the suffixes of `code_suffixes`
(spec 000078).

Reason: The editor shows the errors of the check at their line while a person writes.

Test: `tests/test_lsp.py`.
