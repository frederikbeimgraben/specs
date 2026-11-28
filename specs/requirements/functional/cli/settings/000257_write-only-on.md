---
id: "000257"
title: A command writes only the parts that are on
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_features.py:test_a_switch_on_writes_the_part_again
  - tests/test_features.py:test_update_follows_the_switches
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

# A command writes only the parts that are on

`spezi init`, `spezi update` and `spezi install` must write or replace only the parts whose
switch is on (spec 000084).

Reason: A part that the project turned off does not come back.

Test: `tests/test_features.py`.
