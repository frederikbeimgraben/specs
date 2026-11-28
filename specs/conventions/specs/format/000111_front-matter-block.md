---
id: "000111"
title: A spec starts with a front matter block
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

# A spec starts with a front matter block

A spec file must start with a front matter block between two `---` lines.

Reason: Every Markdown tool reads standard front matter.

Test: `spezi check`.
