---
id: "000078"
title: specs.toml holds the settings of the specs command
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
tests:
  - tests/test_settings.py:test_a_bad_setting_stops_each_command
implementation:
  - src/specs_kit/project.py
  - src/specs_kit/data/specs.toml
scope:
  - src/specs_kit/
  - specs.toml
---

# specs.toml holds the settings of the specs command

`specs` must read its settings from `specs.toml` in the root of the project. Each key is
optional and must have this type and default:

| Key | Type | Default | Meaning |
| --- | --- | --- | --- |
| `forge` | string | `github` | `github`, `gitlab` or `codeberg` (000066). |
| `base_ref` | string | `origin/main` | The base branch (000013). |
| `code_dirs` | list of strings | `[]` | The folders with `§` references (000017). |
| `code_suffixes` | list of strings | `.py`, `.ts`, `.js`, `.go`, `.rs`, `.java`, `.kt`, `.nix`, `.sh` | The file types in `code_dirs`. |
| `max_elements` | whole number from 1 | `25` | The highest count of elements in one diagram (000037). |
| `[upstream."<repo>"]` | table | none | One table for each copy, with `ref` (string) and the optional `include` (list of strings) (000048). |

The template `src/specs_kit/data/specs.toml` must hold each key with its default and a comment.
When `specs.toml` is no valid TOML, or a key has a different type, each command must stop with
one line `specs: specs.toml: <error>` and the exit code 1.

Reason: One table tells every key, and a wrong type stops the command before it reads the wrong
folders.

Test: `tests/test_settings.py`.
