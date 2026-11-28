---
id: "000113"
title: The front matter has no other keys
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
  - src/spezi/project.py
scope:
  - specs/
---

# The front matter has no other keys

The front matter must not have a key that is not in the table of (spec 000009).

Reason: One fixed set of keys lets one tool read every spec.

Test: `spezi check`.
