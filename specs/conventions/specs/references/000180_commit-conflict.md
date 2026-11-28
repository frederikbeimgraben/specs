---
id: "000180"
title: Two commits of a transitive upstream are an error
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_transitive.py:test_two_commits_of_one_upstream_are_an_error
implementation:
  - src/spezi/transitive.py
  - src/spezi/kit.py
  - src/spezi/check.py
scope:
  - specs/
  - spezi.toml
---

# Two commits of a transitive upstream are an error

When two direct upstreams name different commits of the same transitive upstream,
`spezi check` must show an error. The error names the repository and both direct upstreams.

Reason: A conflict of two commits needs a decision of a person.

Test: `tests/test_transitive.py`.
