---
id: "000076"
title: spezi formats its output for a terminal
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_output.py:test_terminal_output_has_color
  - tests/test_output.py:test_a_migration_has_a_blue_mark
  - tests/test_output.py:test_each_repository_has_a_green_mark
implementation:
  - src/spezi/cli.py
  - src/spezi/view.py
scope:
  - src/spezi/
---

# spezi formats its output for a terminal

When stdout is a terminal, each command of `spezi` except `mcp` and `lsp` must print a formatted
output:

| Command | Formatted output |
| --- | --- |
| `check` | Each error in red, then each warning in yellow with `! ` (spec 000093), then the line with the counts (spec 000214). |
| `list`, `search` | A table with the columns (spec 000229), with a color for each status. |
| `show` | The front matter as YAML and the body as rendered Markdown. |
| `resolve` | The long form in color. |
| `init`, `install`, `update`, `add`, `configure`, `remove`, `new`, `setup-ide` | Each line of the message with a green mark. Below it, each line of a repository (spec 000067, 000289) with a green mark. Then each migration that ran (spec 000282) on its own line with a blue mark `↻` and without `migrated:`. |

Reason: A person reads the formatted output faster.

Test: `tests/test_output.py`.
