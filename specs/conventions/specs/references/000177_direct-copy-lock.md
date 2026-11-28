---
id: "000177"
title: The copy of a direct upstream holds its spezi.lock
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

# The copy of a direct upstream holds its spezi.lock

The copy of each direct upstream (spec 000092) must hold its `spezi.lock` as
`specs/.upstream/<repo>/spezi.lock`, with no change.

Reason: The copy of `spezi.lock` lets the check find a conflict without a network.

Test: `spezi check`.
