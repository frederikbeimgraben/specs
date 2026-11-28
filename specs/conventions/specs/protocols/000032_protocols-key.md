---
id: "000032"
title: A rule names the formats that it uses
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# A rule names the formats that it uses

A functional or non-functional spec can send, read or store the format of a protocol spec. Then
it must list the full ID of that protocol spec in `protocols`.

Reason: A reader of a rule finds the exact format. A tool finds every rule that a change of a
format affects.

Test: Review.
