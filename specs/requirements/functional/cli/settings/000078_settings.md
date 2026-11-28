---
id: "000078"
title: spezi.toml holds the settings of the spezi command
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_settings.py:test_a_bad_setting_stops_each_command
  - tests/test_settings.py:test_an_unknown_key_of_a_copy_stops_each_command
implementation:
  - src/spezi/project.py
  - src/spezi/data/spezi.toml
scope:
  - src/spezi/
  - spezi.toml
---

# spezi.toml holds the settings of the spezi command

`spezi` must read its settings from `spezi.toml` in the root of the project. Each key is
optional and must have this type and default:

| Key | Type | Default | Meaning |
| --- | --- | --- | --- |
| `repo` | string | none | The full name of the project, `<host>/<group>/.../<repo>` (spec 000047). A transitive upstream of this name gets no copy (spec 000092). |
| `forge` | string | `github` | `github`, `gitlab` or `codeberg` (spec 000066). |
| `base_ref` | string | `origin/main` | The base branch (spec 000013). |
| `code_dirs` | list of strings | `[]` | The folders with code that refers to rules (spec 000017). |
| `code_suffixes` | list of strings | `.py`, `.ts`, `.js`, `.go`, `.rs`, `.java`, `.kt`, `.nix`, `.sh` | The file types in `code_dirs`. |
| `max_elements` | whole number from 1 | `25` | The highest count of elements in one diagram (spec 000037). |
| `[features]` | table | each switch `true` | The switches of the optional parts of the kit (spec 000084). |
| `[upstream."<repo>"]` | table | none | One table for each direct upstream, with `ref` (string: a tag, a branch or a commit), the optional `include` (list of strings) and the optional `transitive` (list of strings) (spec 000048, 000082, 000092). |

The template `src/spezi/data/spezi.toml` must hold each key with its default and a comment.
When `spezi.toml` is no valid TOML, when a key has a different type, when `forge` is not
`github`, `gitlab` or `codeberg`, or when a key on the top level or in a table
`[upstream."<repo>"]` is not in the table above, each command must stop with one line
`specs: spezi.toml: <error>` and the exit code 1.

Reason: One table tells every key, and a wrong type stops the command before it reads the wrong
folders.

Test: `tests/test_settings.py`.
