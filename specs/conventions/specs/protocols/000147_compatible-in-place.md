---
id: "000147"
title: A compatible change keeps the spec and its version
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/
scope:
  - specs/
---

# A compatible change keeps the spec and its version

A compatible change of a format must change the protocol spec in place. It must keep `version`.

Reason: A receiver of the old version can read the new version.

Test: Review.
