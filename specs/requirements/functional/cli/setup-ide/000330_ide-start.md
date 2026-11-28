---
id: "000330"
title: The extension starts spezi lsp
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/ide.py
  - src/spezi/cli.py
  - src/spezi/kit.py
  - src/spezi/data/editors/
  - flake.nix
scope:
  - src/spezi/
  - flake.nix
---

# The extension starts spezi lsp

The extension (spec 000089) must start `spezi lsp` (spec 000088) from `PATH`. When `PATH` has no
`spezi`, it starts the command in `server.json` of the folder. It starts the server for Markdown
and for the files with the suffixes of `server.json`.

Reason: The extension works with and without a devShell.

Test: `tests/test_setup_ide.py`.
