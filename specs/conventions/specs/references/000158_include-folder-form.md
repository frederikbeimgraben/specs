---
id: "000158"
title: A folder of include is a path of kebab-case folders
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/changes.py
  - src/spezi/check.py
  - src/spezi/kit.py
  - src/spezi/install.py
scope:
  - specs/
---

# A folder of include is a path of kebab-case folders

A folder of `include` (spec 000157) must be a path of kebab-case folder names below
`specs/`.

Reason: The folder names are part of the rule IDs (spec 000005).

Test: `spezi check`.
