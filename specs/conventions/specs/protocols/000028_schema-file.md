---
id: "000028"
title: A JSON format has a JSON Schema file beside its spec
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - src/spezi/check.py
  - src/spezi/sections.py
scope:
  - specs/
---

# A JSON format has a JSON Schema file beside its spec

A protocol spec with the media type `application/json` or a `+json` media type must have a
schema file beside it. The schema file must have the name of the spec file with `.schema.json`
instead of `.md`. The schema must use JSON Schema 2020-12 and must set `$schema` to
`https://json-schema.org/draft/2020-12/schema`.

A person must write the schema file. A script must not write it from the code.

A format that is not JSON must not have a schema file. Its `## Schema` section must hold a table
of its parts. Every `.json` file below `specs/protocols/` must be the schema file of a protocol
spec.

Reason: The schema exists before the code (000002). One schema language lets one validator
check every example and every implementation.

Test: `spezi check` checks the file, `$schema` and the schema itself.
