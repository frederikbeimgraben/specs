---
id: "000032"
title: A rule names the formats that it uses
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-23
implementation:
  - scripts/check_specs.py
scope:
  - specs/
---

# A rule names the formats that it uses

A functional or non-functional spec that sends, reads or stores the format of a protocol spec
must list the full ID of that protocol spec in `protocols`. A spec that uses no such format must
not have the key `protocols`. Each entry must name a protocol spec that is in force.

Reason: A reader of a rule finds the exact format. A tool finds every rule that a change of a
format affects.

Test: `scripts/check_specs.py` checks every entry of `protocols`.
