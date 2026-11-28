---
id: "000306"
title: include holds no folder below a different folder of include
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/kit.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# include holds no folder below a different folder of include

`spezi add` must not write a folder to `include` when a different folder of `include` holds it.

Reason: The copy of the outer folder holds the inner folder.

Test: Review.
