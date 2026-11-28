---
id: "000118"
title: replaced_by lists each rule that replaces the rule
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# replaced_by lists each rule that replaces the rule

`replaced_by` of a replaced rule must list each rule of the same repository that names it in
`replaces`, and no other rule.

Reason: A reader of the old rule finds the rule in force.

Test: `spezi check` checks `replaced_by`.
