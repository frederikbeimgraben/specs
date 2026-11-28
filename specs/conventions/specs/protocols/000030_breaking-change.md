---
id: "000030"
title: A breaking change of a format is a new protocol spec
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# A breaking change of a format is a new protocol spec

A breaking change of a format must be a new protocol spec with a new number and `version` plus
one.

Reason: A receiver that names the ID of a format must find the same contract later.

Test: Review.
