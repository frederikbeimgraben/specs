---
id: "000179"
title: One commit of a transitive upstream gives the union of include
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_transitive.py:test_union_of_folders
implementation:
  - src/spezi/transitive.py
  - src/spezi/kit.py
  - src/spezi/check.py
scope:
  - specs/
  - spezi.toml
---

# One commit of a transitive upstream gives the union of include

When two direct upstreams name the same transitive upstream with the same commit, the copy must
hold the union of the two `include` lists. An empty `include` is all rules.

Reason: Each direct upstream gets the rules that it refers to.

Test: `tests/test_transitive.py`.
