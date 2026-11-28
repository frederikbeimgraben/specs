---
id: "000086"
title: spezi configure changes the settings in spezi.toml
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_configure.py:test_configure_sets_a_switch
  - tests/test_configure.py:test_configure_keeps_the_comments
  - tests/test_configure.py:test_configure_stops_for_a_bad_value
  - tests/test_configure.py:test_configure_stops_for_claude_without_agents
  - tests/test_configure.py:test_configure_needs_a_terminal_or_a_key
  - tests/test_configure.py:test_the_menu_saves_the_changes
  - tests/test_configure.py:test_the_menu_discards_the_changes
implementation:
  - src/spezi/configure.py
  - src/spezi/settings.py
  - src/spezi/cli.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# spezi configure changes the settings in spezi.toml

`spezi configure` must show a menu on a terminal. The menu must show each key of the table below
with its value. It must also show one line for each repository of `[upstream]` with its `ref`
and its `include`, and the items `add a repository`, `save` and `discard`.

| Item | Question |
| --- | --- |
| `forge` | One of `github`, `gitlab` and `codeberg` |
| `base_ref`, `max_elements` | A text, with a check of its type (spec 000078) |
| `code_dirs`, `code_suffixes` | The checklists (spec 000085), with the values of `spezi.toml` checked |
| `features.<switch>` | None. The item changes the switch from `true` to `false` or back. |
| A repository | `ref` with the choices of `spezi add`, the folders with the checklist of `spezi add`, or `remove`. The kit has no `remove`. |
| `add a repository` | The questions of `spezi add` for `<repo>`, `<ref>` and the folders |

After an item, the command must show the menu again. A change must stay in memory until
`save`. `save` must stop with the error and show the menu again when the settings break a rule
(spec 000078, 000084), for example `claude` on with `agents` off. Else it must write
`spezi.toml` and do the steps of `spezi install` (spec 000083). `discard` must ask once when a value
changed, and must then stop without a change. Ctrl+C must stop without a change.

`spezi configure <key> <value>` must set one key without questions and then do the steps of
`spezi install`. `<key>` must be `forge`, `base_ref`, `code_dirs`, `code_suffixes`,
`max_elements` or `features.<switch>`. `<value>` must have the plain form of its key: `true` or
`false`, a whole number, a text, or a list with a comma between the entries, for example
`src,lib`. The command must stop with an error and change no file for a different key or for a
value of a different form. It must do the same for a value that breaks a rule
(spec 000078, 000084). Without a terminal, or with `-y`, `spezi configure` must stop with an
error when it has no key and value.

`spezi configure` must change only the values in `spezi.toml`. The comments, the order of the
keys and the lines that it does not change must stay.

Reason: A person changes a setting without the TOML syntax, and the comments of the template
stay. A script or an agent sets one value with one command.

Test: `tests/test_configure.py`.
