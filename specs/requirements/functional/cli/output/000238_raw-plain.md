---
id: "000238"
title: Raw output is plain text
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_output.py:test_raw_output_has_no_color
implementation:
  - src/spezi/cli.py
  - src/spezi/view.py
scope:
  - src/spezi/
---

# Raw output is plain text

With the option `--raw` after the command, or when stdout is not a terminal, a command must print
the plain text of its own spec. The plain text has no color and no table.

Reason: A script, the CI and an agent read the plain text, and it stays the same.

Test: `tests/test_output.py`.
