---
id: "000308"
title: spezi add copies the chosen transitive upstreams
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_transitive.py:test_add_with_recursive_copies_the_transitive_upstream
  - tests/test_transitive.py:test_add_without_recursive_copies_no_transitive_upstream
implementation:
  - src/spezi/kit.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# spezi add copies the chosen transitive upstreams

`spezi add` must copy the transitive upstreams (spec 000092) that the user chooses (spec 000085).
It writes them as `transitive` to the table. With `-r` (also `--recursive`), it copies each
transitive upstream without a question.

Reason: With `-r`, a script copies the rules that the rules of `<repo>` refer to, without a
question.

Test: `tests/test_transitive.py`.
