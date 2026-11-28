---
id: "000252"
title: A path in JSON is relative
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/data.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# A path in JSON is relative

Each path in the JSON output (spec 000080) must be relative to the root of the project.

Reason: The output is the same on each computer.

Test: Review.
