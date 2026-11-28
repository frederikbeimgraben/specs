---
id: "000132"
title: Below the kind folder are the area and the topic
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# Below the kind folder are the area and the topic

Below the kind folder (spec 000004), the first folder must be the area, for example
`meetings/`. The folder below the area must be the topic, for example `voting/`. The topic
folder holds the rule files.

Reason: Area and topic put the rules of one part of the product side by side.

Test: `spezi check`.
