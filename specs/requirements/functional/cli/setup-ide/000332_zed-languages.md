---
id: "000332"
title: Each suffix has its Zed language
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_setup_ide.py:test_zed_gets_the_source_of_the_extension
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

# Each suffix has its Zed language

In `extension.toml` (spec 000089), each suffix must have its language name of Zed:

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

For a suffix without a language name, the command shows a hint and skips the suffix.

Reason: Zed starts a language server only for a language name.

Test: `tests/test_setup_ide.py`.
