---
id: "000076"
title: specs formats its output for a terminal
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
tests:
  - tests/test_output.py:test_terminal_output_has_color
  - tests/test_output.py:test_raw_output_has_no_color
implementation:
  - src/specs_kit/cli.py
  - src/specs_kit/view.py
scope:
  - src/specs_kit/
---

# specs formats its output for a terminal

When stdout is a terminal, each command of `specs` except `mcp` must print a formatted output:

| Command | Formatted output |
| --- | --- |
| `check` | Each error in red, then the count of specs and errors, green without errors. |
| `list`, `search` | A table with the columns of 000072, with a color for each status. |
| `show` | The front matter as YAML and the body as rendered Markdown. |
| `resolve` | The long form in color. |
| `init`, `update`, `add`, `new` | The message with a green mark. |

With the option `--raw` after the command, or when stdout is not a terminal, the command must
print the plain text of its own spec, with no color and no table. With `--json`, the command
must print JSON (000080). The MCP server must always return the plain text.

Reason: A person reads the formatted output faster. A script, the CI and an agent read the plain
text, and it stays the same.

Test: `tests/test_output.py`.
