---
id: "000089"
title: spezi setup-ide adds the language server to Zed or VS Code
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_setup_ide.py:test_update_writes_the_folder_again
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

# spezi setup-ide adds the language server to Zed or VS Code

`spezi setup-ide zed|code [-y]` must write the extension of the editor to a folder of the
project:

| Editor | Folder | Files |
| --- | --- | --- |
| `zed` | `.zed/spezi/` | The source of the Zed extension: `extension.toml`, `Cargo.toml` and `src/lib.rs`, and `server.json`. |
| `code` | `.vscode/spezi/` | `spezi.vsix`, which the flake of the kit builds, and `server.json`. |

Reason: A person adds the language server to the editor with one command.

Test: `tests/test_setup_ide.py`.
