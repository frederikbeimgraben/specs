---
id: "000049"
title: Each rule of a different repository applies unless it is excluded
kind: convention
status: draft
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - scripts/check_specs.py
scope:
  - specs/
---

# Each rule of a different repository applies unless it is excluded

Each rule of a copy of 000048 with the status `draft` or `approved` must apply to the project.
A rule that must not apply must be in `exclude` of its repository in `specs/config.toml`, with
the reason as the value. A reference must not point to an excluded rule.

Reason: A new rule of the different repository applies after the next update. An exception is
a decision at one place, with its reason.

Test: `scripts/check_specs.py` checks that each excluded ID exists in the copy and that no
reference points to an excluded rule.
