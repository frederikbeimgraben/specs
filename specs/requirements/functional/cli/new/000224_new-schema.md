---
id: "000224"
title: spezi new writes a schema for a JSON protocol
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_new.py:test_new_writes_a_schema_for_a_json_protocol
implementation:
  - src/spezi/new.py
scope:
  - src/spezi/
---

# spezi new writes a schema for a JSON protocol

For a protocol with a JSON media type, `spezi new` must also write a minimal JSON Schema next to
the spec (spec 000028).

Reason: The schema file of a JSON format exists from the start.

Test: `tests/test_new.py`.
