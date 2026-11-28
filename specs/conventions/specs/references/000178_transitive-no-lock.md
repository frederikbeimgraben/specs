---
id: "000178"
title: The copy of a transitive upstream holds no spezi.lock
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

# The copy of a transitive upstream holds no spezi.lock

The copy of a transitive upstream (spec 000092) must not hold a `spezi.lock`.

Reason: The project copies only one level of upstreams, and their upstreams need no lock.

Test: `spezi check`.
