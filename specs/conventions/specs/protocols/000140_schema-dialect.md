---
id: "000140"
title: A schema uses JSON Schema 2020-12
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

# A schema uses JSON Schema 2020-12

A schema file (spec 000028) must use JSON Schema 2020-12. It must set `$schema` to
`https://json-schema.org/draft/2020-12/schema`.

Reason: One schema language lets one validator examine every example and every
implementation.

Test: `spezi check` checks `$schema` and the schema itself.
