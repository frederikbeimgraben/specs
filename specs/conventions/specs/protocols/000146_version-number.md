---
id: "000146"
title: The version of a format is a whole number from 1
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# The version of a format is a whole number from 1

`version` of a protocol spec must be a whole number from 1.

Reason: A whole number shows the order of the breaking changes (spec 000030).

Test: `spezi check` checks the form of `version`.
