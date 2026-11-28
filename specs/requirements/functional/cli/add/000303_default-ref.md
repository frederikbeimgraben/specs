---
id: "000303"
title: Without a ref, spezi add takes the highest version
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_kit.py:test_add_without_ref_takes_the_default_branch
implementation:
  - src/spezi/kit.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# Without a ref, spezi add takes the highest version

Without `<ref>`, `spezi add` must take or propose the tag with the highest version, for example
`v1.10` before `v1.9`. A tag has a version when it has the form `1.2.3` or `v1.2.3` with one or
more numbers. Without such a tag, the command takes the name of the default branch.

Reason: A version tag is a stable state of the rules.

Test: `tests/test_kit.py`.
