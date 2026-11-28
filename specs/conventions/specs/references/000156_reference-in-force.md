---
id: "000156"
title: A reference names a rule in force
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_check.py:test_check_finds_a_reference_to_a_removed_rule
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# A reference names a rule in force

A reference to a rule of the same repository must name a rule of the project with the status
`draft` or `approved`. This applies to the text of a spec and to the code.

Reason: A reference to a rule that is not in force leads the reader to an old rule.

Test: `spezi check` finds each number in the text of a spec and each `(spec ...)` in the code.
It checks that each of them names a rule with the status `draft` or `approved`.
