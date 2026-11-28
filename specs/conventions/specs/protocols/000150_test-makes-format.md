---
id: "000150"
title: The test makes the format with the code
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/
scope:
  - specs/
---

# The test makes the format with the code

The test of a JSON format that the product writes (spec 000031) must make the format with the
code of the product. It must validate the result against the schema file.

Reason: The schema is the contract, and the code is a second copy of it.

Test: Review.
