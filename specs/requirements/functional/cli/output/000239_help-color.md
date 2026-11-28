---
id: "000239"
title: The help has color
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_output.py:test_help_on_terminal_has_color
  - tests/test_output.py:test_usage_on_terminal_has_color
implementation:
  - src/spezi/cli.py
  - src/spezi/view.py
scope:
  - src/spezi/
---

# The help has color

The help of `spezi` and of each command must have color, with `rich-argparse`:

| Output | Stream | Color |
| --- | --- | --- |
| `--help` | stdout | The program name, commands and options bold cyan, headings bold, metavars cyan. |
| The usage after a wrong argument | stderr | The same colors. |

Reason: A person reads the help faster.

Test: `tests/test_output.py`.
