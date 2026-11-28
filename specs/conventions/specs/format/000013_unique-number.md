---
id: "000013"
title: The number is the identity of a rule
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
  - spezi.toml
scope:
  - specs/
---

# The number is the identity of a rule

The number must be unique over all specs of the repository. The rules of a different
repository keep their numbers (spec 000047). The number is the real ID. Kind and path only make
the ID readable.

Reason: An old reference must not point to a different rule, also after a file moves.

Test: `spezi check`: no number occurs two times.
