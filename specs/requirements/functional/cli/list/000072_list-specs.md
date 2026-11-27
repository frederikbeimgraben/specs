---
id: "000072"
title: specs list prints every rule
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
implementation:
  - src/specs_kit/queries.py
scope:
  - src/specs_kit/
---

# specs list prints every rule

`specs list` must print one line for each rule of the project, then one line for each rule of
the copies. A line must hold the long form, the status and the title, separated by tabs.

Reason: An agent sees all rules in one call.
