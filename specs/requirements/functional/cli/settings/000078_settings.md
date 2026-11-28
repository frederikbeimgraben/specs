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
  - tests/test_settings.py:test_init_writes_the_settings_without_comments
  - tests/test_migrations.py:test_migration_6_removes_the_comments_of_the_template
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
| `repo` | string | none | The full name of the project, `<host>/<group>/.../<repo>` (000047). A transitive upstream of this name gets no copy (000092). |
| `forge` | string | `github` | `github`, `gitlab` or `codeberg` (000066). |
| `base_ref` | string | `origin/main` | The base branch (000013). |
| `code_dirs` | list of strings | `[]` | The folders with `§` references (000017). |
| `code_suffixes` | list of strings | `.py`, `.ts`, `.js`, `.go`, `.rs`, `.java`, `.kt`, `.nix`, `.sh` | The file types in `code_dirs`. |
| `max_elements` | whole number from 1 | `25` | The highest count of elements in one diagram (000037). |
| `own` | list of strings | `[]` | The folders below `specs/` with the rules of this repository only. A copy of the repository leaves them out (000048). |
| `[features]` | table | each switch `true` | The switches of the optional parts of the kit (000084). |
| `[upstream."<repo>"]` | table | none | One table for each direct upstream, with `ref` (string: a tag, a branch or a commit), the optional `include` (list of strings) and the optional `transitive` (list of strings) (000048, 000082, 000092). |

The template `src/spezi/data/spezi.toml` must hold each key with its default and no comment.
A migration (000081) must remove each line of `spezi.toml` that is a comment of an earlier
template. A different comment must stay.
When `spezi.toml` is no valid TOML, when a key has a different type, when `forge` is not
`github`, `gitlab` or `codeberg`, or when a key on the top level or in a table
`[upstream."<repo>"]` is not in the table above, each command must stop with one line
`specs: spezi.toml: <error>` and the exit code 1.

Reason: One table tells every key, and a wrong type stops the command before it reads the wrong
folders.

Test: `tests/test_settings.py`.
