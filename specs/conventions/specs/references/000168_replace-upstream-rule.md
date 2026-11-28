---
id: "000168"
title: A project rule replaces a rule of a copy that must not apply
kind: convention
status: draft
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# A project rule replaces a rule of a copy that must not apply

A project rule must name in `replaces` each rule of a copy that is not for the project. That
project rule has the status `draft` or `approved`.

Reason: The project rule that replaces it holds the reason, and the owner approves it like each
other rule.

Test: `spezi check` checks that each entry of `replaces` exists in the copy.
