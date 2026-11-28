---
id: "000157"
title: include limits the copy to its folders
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

# include limits the copy to its folders

When the table of the repository in `spezi.toml` has `include`, the copy (spec 000048) must
hold only the folders below `specs/` that `include` names. An example is
`include = ["style/python/"]`.

Reason: A project takes only the rules that it needs, and an agent cannot read and follow the
other rules.

Test: `spezi check` checks that each folder of `include` is in the copy. It also checks that the
copy holds no file outside these folders other than `spezi.lock`.
