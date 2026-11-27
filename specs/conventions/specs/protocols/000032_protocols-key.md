---
id: "000032"
title: A rule names the formats that it uses
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - src/specs_kit/check.py
scope:
  - specs/
---

# A rule names the formats that it uses

A functional or non-functional spec that sends, reads or stores the format of a protocol spec
must list the full ID of that protocol spec in `protocols`. A spec that uses no such format must
not have the key `protocols`. Each entry must name a protocol spec that is in force.

Reason: A reader of a rule finds the exact format. A tool finds every rule that a change of a
format affects.

Test: `specs check` checks every entry of `protocols`.
