---
id: "000263"
title: An unknown switch is an error
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/project.py
  - src/spezi/install.py
  - src/spezi/kit.py
  - src/spezi/devshell.py
  - src/spezi/check.py
  - src/spezi/data/spezi.toml
scope:
  - src/spezi/
  - spezi.toml
---

# An unknown switch is an error

A key of `[features]` that is not in the table of the switches (spec 000084) must be an error of
`spezi.toml` (spec 000255). A value that is not `true` or `false` must also be an error.

Reason: A typing error in a switch name otherwise has no effect.

Test: Review.
