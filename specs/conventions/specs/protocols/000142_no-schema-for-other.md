---
id: "000142"
title: A format that is not JSON has no schema file
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
  - src/spezi/sections.py
scope:
  - specs/
---

# A format that is not JSON has no schema file

A protocol spec of a format that is not JSON must not have a schema file.

Reason: JSON Schema describes only JSON.

Test: `spezi check`.
