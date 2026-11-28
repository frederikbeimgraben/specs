---
id: "000021"
title: The rule text uses must and must not
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# The rule text uses must and must not

Use `must` for an obligation and `must not` for a prohibition. Use the present tense for a fact
that the rule depends on.

Reason: One fixed word shows what is binding and what is a fact.

Test: `spezi check` finds a draft or approved rule without `must`.
