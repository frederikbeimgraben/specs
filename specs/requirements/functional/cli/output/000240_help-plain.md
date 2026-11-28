---
id: "000240"
title: The help has color only on a terminal
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_output.py:test_help_with_no_color_has_no_color
  - tests/test_output.py:test_help_in_a_pipe_has_no_color
implementation:
  - src/spezi/cli.py
  - src/spezi/view.py
scope:
  - src/spezi/
---

# The help has color only on a terminal

The help must have color only when its stream is a terminal and `NO_COLOR` is not set. Else the
help must be plain text.

Reason: A pipe and a person who sets `NO_COLOR` get no color codes.

Test: `tests/test_output.py`.
