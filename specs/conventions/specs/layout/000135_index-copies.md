---
id: "000135"
title: The index lists the rules of the copies
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
  - src/spezi/index.py
scope:
  - specs/
---

# The index lists the rules of the copies

A second section of the index (spec 000007) must list every rule of the copies (spec 000048)
that applies (spec 000049). Each rule has the long form of its ID (spec 000047).

Reason: A reader also finds the rules of the other repositories on one page.

Test: `spezi check` fails when `specs/README.md` is not current.
