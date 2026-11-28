---
id: "000076"
title: spezi formats its output for a terminal
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_output.py:test_terminal_output_has_color
  - tests/test_output.py:test_raw_output_has_no_color
  - tests/test_output.py:test_a_migration_has_a_blue_mark
  - tests/test_output.py:test_each_repository_has_a_green_mark
  - tests/test_output.py:test_help_on_terminal_has_color
  - tests/test_output.py:test_usage_on_terminal_has_color
  - tests/test_output.py:test_help_with_no_color_has_no_color
  - tests/test_output.py:test_help_in_a_pipe_has_no_color
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
| `check` | Each error in red, then the line with the counts of 000065, green without errors. |
| `list`, `search` | A table with the columns of 000072, with a color for each status. |
| `show` | The front matter as YAML and the body as rendered Markdown. |
| `resolve` | The long form in color. |
| `init`, `update`, `add`, `new`, `setup-ide` | Each line of the message with a green mark. Below it, each line of a repository (000067, 000083) with a green mark, and each migration that ran (000081) on its own line with a blue mark `↻` and without `migrated:`. |

With the option `--raw` after the command, or when stdout is not a terminal, the command must
print the plain text of its own spec, with no color and no table. With `--json`, the command
must print JSON (000080). The MCP server must always return the plain text.

The help of `spezi` and of each command must have color, with `rich-argparse`:

| Output | Stream | Color |
| --- | --- | --- |
| `--help` | stdout | The program name, commands and options bold cyan, headings bold, metavars cyan. |
| The usage after a wrong argument | stderr | The same colors. |

The help must have color only when its stream is a terminal and `NO_COLOR` is not set. Else
the help must be plain text.

Reason: A person reads the formatted output and the help faster. A script, the CI and an agent
read the plain text, and it stays the same.

Test: `tests/test_output.py`.
