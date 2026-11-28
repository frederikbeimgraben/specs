---
id: "000176"
title: Each repository of transitive gets a copy or a skip
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_transitive.py:test_the_project_itself_gets_no_copy
implementation:
  - src/spezi/transitive.py
  - src/spezi/kit.py
  - src/spezi/check.py
scope:
  - specs/
  - spezi.toml
---

# Each repository of transitive gets a copy or a skip

For each repository of `transitive` (spec 000092), these rules must apply:

| Case | Effect |
| --- | --- |
| The repository is `repo` of `spezi.toml`, the project itself. | No copy. |
| The repository has its own table in `spezi.toml`. | No copy from `transitive`. The direct table wins. |
| Else | A copy below `specs/.upstream/<repo>/` (spec 000048), at the `commit` that the `spezi.lock` of the direct upstream names for it, with its `include` from that entry. |

Reason: `repo` stops a cycle, for example when two repositories copy the rules of each other. The
commit of the `spezi.lock` of the upstream is the commit that the upstream checked its rules
against.

Test: `spezi check` checks that each repository of `transitive` has a copy, or that the table
skips it. The check uses no network.
