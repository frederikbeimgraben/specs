---
id: "000223"
title: spezi new takes the owner from the option or from git
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/new.py
scope:
  - src/spezi/
---

# spezi new takes the owner from the option or from git

`spezi new` must take the owner from `--owner`, else from `git config <forge>.user`. Without an
owner, the command must stop with an error and write no file.

Reason: Each spec has an owner who approves it (spec 000009).

Test: `tests/test_new.py`.
