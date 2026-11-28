---
id: "000048"
title: The rules of a different repository are an unchanged copy
kind: convention
status: draft
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_kit.py:test_a_copy_keeps_a_folder_named_upstream
implementation:
  - src/spezi/changes.py
  - src/spezi/check.py
  - src/spezi/kit.py
  - src/spezi/install.py
scope:
  - specs/
---

# The rules of a different repository are an unchanged copy

The rules of a different repository must be a copy of its `specs/` folder below
`specs/.upstream/<host>/<group>/.../<repo>/`.

Reason: The copy lets an agent and the check read the rules without a network.

Test: `spezi check` checks that each repository of `spezi.toml` has a copy, and that each copy
has a repository in `spezi.toml` or in a list `transitive` (spec 000092).
