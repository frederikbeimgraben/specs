---
id: "000182"
title: A copy of a transitive upstream follows the copy rules
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/transitive.py
  - src/spezi/kit.py
  - src/spezi/check.py
scope:
  - specs/
  - spezi.toml
---

# A copy of a transitive upstream follows the copy rules

A copy of a transitive upstream must follow the same rules as a copy of a direct upstream
(spec 000048, 000049).

Reason: An agent reads both copies in the same way.

Test: `spezi check`.
