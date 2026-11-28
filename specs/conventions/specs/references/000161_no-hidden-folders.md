---
id: "000161"
title: A copy leaves out the hidden folders
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

# A copy leaves out the hidden folders

The copy (spec 000048) must not hold the hidden folders of the repository, for example
`specs/.upstream/`.

Reason: A hidden folder holds files of the kit or copies of a third repository, and no rules of
the repository.

Test: `spezi check`.
