---
id: "000258"
title: spezi install removes the parts that are off
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_features.py:test_a_switch_off_removes_the_part
  - tests/test_features.py:test_a_changed_claude_file_stays
implementation:
  - src/spezi/project.py
  - src/spezi/install.py
  - src/spezi/kit.py
  - src/spezi/devshell.py
  - src/spezi/check.py
  - src/spezi/data/spezi.toml
scope:
  - src/spezi/
  - spezi.toml
---

# spezi install removes the parts that are off

`spezi install` must remove each part whose switch is off, as the table of the switches tells
(spec 000084).

Reason: A switch that goes off takes the part out of the project.

Test: `tests/test_features.py`.
