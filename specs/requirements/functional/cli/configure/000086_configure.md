---
id: "000086"
title: spezi configure changes the settings in spezi.toml
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
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

Reason: A person changes a setting without the TOML syntax.

Test: `tests/test_configure.py`.
