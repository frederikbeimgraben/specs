---
id: "000029"
title: The example of a JSON format matches its schema
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
implementation:
  - src/specs_kit/check.py
scope:
  - specs/
---

# The example of a JSON format matches its schema

The `## Example` section must hold at least one complete example in a code block. For a JSON
format, every `json` code block in `## Example` must match the schema file. The check ignores
other code blocks, for example the headers of a request in an `http` block.

Reason: A receiver copies the example first. An example that CI checks cannot drift from the
schema.

Test: `specs check` validates every `json` code block of `## Example`.
