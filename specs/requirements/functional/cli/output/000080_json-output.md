---
id: "000080"
title: spezi prints its data as JSON
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_json.py:test_list_and_resolve_give_rules
  - tests/test_json.py:test_show_gives_meta_and_body
implementation:
  - src/spezi/data.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# spezi prints its data as JSON

With the option `--json` after the command, each command of `spezi` except `mcp` and `lsp` must
print its data as JSON, indented with two spaces, also on a terminal.

| Command | JSON |
| --- | --- |
| `list`, `search` | A list with one rule object for each line (spec 000229). |
| `resolve` | The rule object. |
| `show` | `long`, `path`, `meta` with the front matter as an object, and `body` with the text after the front matter. |
| `check` | `specs` with the count of the rules of the project, `upstream` with the count of the rules of the copies (spec 000214), `errors`, `warnings` (spec 000093), and `changed` (spec 000077). |
| `init`, `install`, `update`, `add`, `configure`, `remove`, `new`, `setup-ide` | `message`, `hints`, `check` with `specs`, `upstream`, `errors` and `warnings` or `null`, and `changed`. |

Reason: A script reads every command in the same way, without parsing text.

Test: `tests/test_json.py`.
