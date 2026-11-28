---
id: "000089"
title: spezi setup-ide adds the language server to Zed or VS Code
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_setup_ide.py:test_zed_gets_the_source_of_the_extension
  - tests/test_setup_ide.py:test_code_gets_the_vsix
  - tests/test_setup_ide.py:test_the_folder_goes_to_gitignore
  - tests/test_setup_ide.py:test_a_tracked_folder_stays_out_of_gitignore
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
project. The extension must start `spezi lsp` (spec 000088) from `PATH`. When `PATH` has no `spezi`,
the extension must start the command in `server.json` of the folder.

| Editor | Folder | Files |
| --- | --- | --- |
| `zed` | `.zed/spezi/` | The source of the Zed extension: `extension.toml`, `Cargo.toml` and `src/lib.rs`, and `server.json`. |
| `code` | `.vscode/spezi/` | `spezi.vsix`, which the flake of the kit builds, and `server.json`. |

`server.json` must hold `command`, the absolute path of the `spezi` program that runs the
command, and `suffixes`, the suffixes of `code_suffixes` (spec 000078). The extension must start the
server for Markdown and for the files with these suffixes. In `extension.toml`, each suffix must
have its language name of Zed:

| Suffix | Language |
| --- | --- |
| `.py` | Python |
| `.ts` | TypeScript |
| `.js` | JavaScript |
| `.go` | Go |
| `.rs` | Rust |
| `.java` | Java |
| `.kt` | Kotlin |
| `.nix` | Nix |
| `.sh` | Shell Script |

For a suffix without a language name, the command must show a hint and skip the suffix.

The command must write the whole folder again when it exists. It must add the folder to
`.gitignore`, except when git tracks a file of the folder or the folder is ignored already.

For `code`, the command must then ask, with the questions (spec 000085), whether to run
`code --install-extension .vscode/spezi/spezi.vsix`. With `-y` or without a terminal, it must
only show this command. For `zed`, it must show that the Zed action `zed: install dev extension`
with the folder `.zed/spezi/` installs the extension, and that Zed needs rustup to build it.
The command must stop with an error and change no file when the program has no `spezi.vsix`.

Reason: A person adds the language server to the editor with one command. The folder stays out
of git, because `server.json` holds a path of one computer.

Test: `tests/test_setup_ide.py`.
