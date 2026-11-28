---
id: "000237"
title: The color of the count line tells the result
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/cli.py
  - src/spezi/view.py
scope:
  - src/spezi/
---

# The color of the count line tells the result

On a terminal, the count line of `spezi check` (spec 000214) must be green without
errors and warnings, yellow with only warnings, else red.

Reason: A person sees the result without reading the numbers.

Test: `tests/test_output.py`.
