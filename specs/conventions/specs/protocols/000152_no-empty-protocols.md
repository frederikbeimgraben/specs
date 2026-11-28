---
id: "000152"
title: A spec without a format has no key protocols
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# A spec without a format has no key protocols

A spec that uses no format of a protocol spec must not have the key `protocols`.

Reason: An empty key tells nothing.

Test: `spezi check`.
