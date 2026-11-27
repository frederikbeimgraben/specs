---
id: "000039"
title: A rule names the structures that it uses
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - src/specs_kit/check.py
scope:
  - specs/
---

# A rule names the structures that it uses

A functional or non-functional spec that depends on a structure of a structure spec must list
the full ID of that structure spec in `structures`. A spec that uses no structure must not have
the key `structures`. Each entry must name a structure spec that is in force.

Reason: A reader of a rule finds the structure that the rule talks about. A tool finds every
rule that a change of the structure affects.

Test: `specs check` checks every entry of `structures`.
