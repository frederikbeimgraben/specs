---
id: "000172"
title: ref names a tag, a branch or a commit
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/lock.py
  - src/spezi/check.py
  - src/spezi/kit.py
scope:
  - src/spezi/lock.py
  - spezi.toml
---

# ref names a tag, a branch or a commit

`ref` in the table of a repository in `spezi.toml` must name a tag, a branch or a commit of the
repository.

Reason: git resolves each of these to one commit (spec 000082).

Test: `spezi update` stops when git cannot resolve `ref`.
