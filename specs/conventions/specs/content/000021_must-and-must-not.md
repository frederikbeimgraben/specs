---
id: "000021"
title: The rule text uses must and must not
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# The rule text uses must and must not

A rule must use `must` for an obligation and `must not` for a prohibition.

Reason: One fixed word shows what is binding.

Test: `spezi check` finds a draft or approved rule without `must`.
