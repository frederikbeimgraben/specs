---
id: "000151"
title: The test of a read format validates its fixture
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/
scope:
  - specs/
---

# The test of a read format validates its fixture

The test of a JSON format that the product reads (spec 000031) must validate its input fixture
against the schema file.

Reason: A fixture that does not match the schema tests a different format.

Test: Review.
