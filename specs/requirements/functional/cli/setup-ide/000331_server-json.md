---
id: "000331"
title: server.json holds the program and the suffixes
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

# server.json holds the program and the suffixes

`server.json` (spec 000089) must hold `command`, the absolute path of the `spezi` program that
runs the command, and `suffixes`, the suffixes of `code_suffixes` (spec 000078).

Reason: The extension finds the program and the files to serve without a setting of its own.

Test: `tests/test_setup_ide.py`.
