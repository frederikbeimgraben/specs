---
id: "000039"
title: A rule names the structures that it uses
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# A rule names the structures that it uses

A functional or non-functional spec that depends on a structure of a structure spec must list
the full ID of that structure spec in `structures`.

Reason: A reader of a rule finds the structure that the rule talks about. A tool finds every
rule that a change of the structure affects.

Test: Review.
