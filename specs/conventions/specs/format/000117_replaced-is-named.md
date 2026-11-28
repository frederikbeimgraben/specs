---
id: "000117"
title: A replaced rule is in replaces of a rule in force
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# A replaced rule is in replaces of a rule in force

A rule with `status: replaced` must be in `replaces` of a rule with the status `draft` or
`approved`.

Reason: The new rule names the old rule, because the copy of a different repository must not
change (spec 000048).

Test: `spezi check` checks `replaces`.
