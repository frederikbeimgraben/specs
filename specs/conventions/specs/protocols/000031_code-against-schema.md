---
id: "000031"
title: A test checks the output of the code against the schema
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/
scope:
  - specs/
---

# A test checks the output of the code against the schema

A protocol spec of a JSON format with `implementation` must list at least one test in `tests`.

Reason: Only a test that runs the code finds the drift between the schema and the code.

Test: Review.
