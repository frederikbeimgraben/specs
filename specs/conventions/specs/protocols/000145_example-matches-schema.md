---
id: "000145"
title: A JSON example matches its schema
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

# A JSON example matches its schema

For a JSON format, every `json` code block in `## Example` must match the schema file
(spec 000028). Other code blocks are not part of this rule, for example the headers of a
request in an `http` block.

Reason: An example that CI checks cannot drift from the schema.

Test: `spezi check` checks every `json` code block of `## Example` against the schema.
