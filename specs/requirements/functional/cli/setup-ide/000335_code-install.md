---
id: "000335"
title: spezi setup-ide code offers to install the extension
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_setup_ide.py:test_code_gets_the_vsix
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

# spezi setup-ide code offers to install the extension

For `code`, `spezi setup-ide` must ask, with the questions (spec 000085), whether to run
`code --install-extension .vscode/spezi/spezi.vsix`. With `-y` or without a terminal, it only
shows this command.

Reason: The person installs the extension with one answer.

Test: `tests/test_setup_ide.py`.
