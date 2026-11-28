---
id: "000197"
title: A spec without a structure has no key structures
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# A spec without a structure has no key structures

A spec that uses no structure of a structure spec must not have the key `structures`.

Reason: An empty key tells nothing.

Test: `spezi check`.
