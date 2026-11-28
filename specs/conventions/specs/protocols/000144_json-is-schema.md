---
id: "000144"
title: Each JSON file below protocols is a schema file
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

# Each JSON file below protocols is a schema file

Each `.json` file below `specs/protocols/` must be the schema file of a protocol spec
(spec 000028).

Reason: A JSON file without its spec is a contract that nobody approved.

Test: `spezi check`.
