---
id: "000245"
title: A copied folder lists only its changed files
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/changes.py
  - src/spezi/cli.py
  - src/spezi/view.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# A copied folder lists only its changed files

For a copied folder, for example `specs/.upstream/`, the list of changed files (spec 000077) must
hold only the files that are new, changed or deleted.

Reason: A copy of many files with few changes gives a short list.

Test: Review.
