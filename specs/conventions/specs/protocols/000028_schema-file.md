---
id: "000028"
title: A JSON format has a JSON Schema file beside its spec
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

# A JSON format has a JSON Schema file beside its spec

A protocol spec with the media type `application/json` or a `+json` media type must have a
schema file beside it. The schema file has the name of the spec file with `.schema.json` instead
of `.md`.

Reason: The schema exists before the code (spec 000002).

Test: `spezi check` checks the file.
