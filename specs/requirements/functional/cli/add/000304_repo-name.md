---
id: "000304"
title: A repository name has a host and one or more groups
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

# A repository name has a host and one or more groups

`<repo>` must have the form `<host>/<group>/.../<repo>` with one or more groups.

Reason: The name is also the path of the copy (spec 000048).

Test: Review.
