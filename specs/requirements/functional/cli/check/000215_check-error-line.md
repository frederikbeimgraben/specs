---
id: "000215"
title: An error line names the path and the line
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_check.py:test_check_gives_the_line
  - tests/test_check.py:test_check_gives_the_line_of_the_key
implementation:
  - src/spezi/agents.py
  - src/spezi/check.py
  - src/spezi/index.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# An error line names the path and the line

An error line of `spezi check` must start with `<path>:<line>: `. The line is the line of the
front matter key, of the entry or of the reference that the error names. Without such a line,
it is 1.

Reason: An editor and a person go to the line of the error.

Test: `tests/test_check.py`.
