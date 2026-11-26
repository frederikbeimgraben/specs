---
id: "000031"
title: A test checks the output of the code against the schema
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - specs/
scope:
  - specs/
---

# A test checks the output of the code against the schema

A protocol spec of a JSON format with `implementation` must list at least one test in `tests`.
The test must make the format with the code of the product and validate the result against
the schema file. A test of a format that the product reads must validate its input fixture the
same way.

Reason: The schema is the contract, and the code is a second copy of it. Only a test that runs
the code finds the drift between the two.

Test: Review.
