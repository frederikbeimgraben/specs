---
id: "000167"
title: No command removes the line of gitattributes
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/changes.py
  - src/spezi/check.py
  - src/spezi/kit.py
  - src/spezi/install.py
scope:
  - specs/
---

# No command removes the line of gitattributes

A command must not remove the line of (spec 000165) from `.gitattributes`, also when no copy
stays.

Reason: A line without a copy does no harm, and a later copy needs it again.

Test: Review.
