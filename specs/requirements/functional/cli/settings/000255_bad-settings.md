---
id: "000255"
title: A bad setting stops each command
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

# A bad setting stops each command

Each command must stop with one line `spezi: spezi.toml: <error>` and the exit code 1 in these
cases:

- `spezi.toml` is no valid TOML.
- A key has a different type.
- `forge` is not `github`, `gitlab` or `codeberg`.
- A key on the top level or in a table `[upstream."<repo>"]` is not in the table of the
  settings (spec 000078).

Reason: A wrong type stops the command before it reads the wrong folders.

Test: `tests/test_settings.py`.
