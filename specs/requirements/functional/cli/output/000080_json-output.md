---
id: "000080"
title: spezi prints its data as JSON
kind: functional
status: draft
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_json.py:test_list_and_resolve_give_rules
  - tests/test_json.py:test_show_gives_meta_and_body
  - tests/test_json.py:test_check_gives_errors_as_objects
  - tests/test_json.py:test_a_command_that_changes_files_gives_all_parts
  - tests/test_json.py:test_a_stop_gives_an_error_object
  - tests/test_json.py:test_raw_and_json_exclude_each_other
implementation:
  - src/spezi/data.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# spezi prints its data as JSON

With the option `--json` after the command, each command of `spezi` except `mcp` and `lsp` must
print its data as JSON, indented with two spaces, also on a terminal. `--json` and `--raw`
(000076) must not go together.

| Command | JSON |
| --- | --- |
| `list`, `search` | A list with one rule object for each line of 000072. |
| `resolve` | The rule object. |
| `show` | `long`, `path`, `meta` with the front matter as an object, and `body` with the text after the front matter. |
| `check` | `specs` with the count of specs, `errors`, and `changed` (000077). |
| `init`, `update`, `add`, `new`, `setup-ide` | `message`, `hints`, `check` with `specs` and `errors` or `null`, and `changed`. |

A rule object must hold `kind` (the kind letter), `id` (the short form of 000047), `long` (the
long form), `status`, `title` and `path`. An error object must hold `file`, `line` (a whole
number from 1), `message` and `rule` (the number of the rule that the error names), and `null`
for a part that the error line does not have. Each object of `changed` must hold `mark` and
`path`. When a command stops with an error, also for a wrong argument, it must print
`{"error": "<error>"}` to stdout, nothing to stderr, and end with the exit code 1. A path must be relative to the root of the
project.

Reason: A script reads every command in the same way, without parsing text.

Test: `tests/test_json.py`.
