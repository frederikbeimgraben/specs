---
id: "000141"
title: A person writes the schema file
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/
scope:
  - specs/
---

# A person writes the schema file

A person must write the schema file (spec 000028). A script must not write it from the code.

Reason: The schema is the contract, and code that writes it copies the errors of the code.

Test: Review.
