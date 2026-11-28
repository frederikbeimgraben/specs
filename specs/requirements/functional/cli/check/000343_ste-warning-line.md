---
id: "000343"
title: A warning line names the path and the line
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_ste.py:test_check_shows_the_findings
implementation:
  - src/spezi/ste.py
  - src/spezi/check.py
  - src/spezi/data/ste/
scope:
  - src/spezi/
---

# A warning line names the path and the line

A warning line of the check of ASD-STE100 (spec 000093) must be
`<path>:<line>: warning: <text>`. The line is the line where the sentence starts.

Reason: An editor and a person go to the sentence.

Test: `tests/test_ste.py`.
