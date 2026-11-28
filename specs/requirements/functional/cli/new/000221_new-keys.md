---
id: "000221"
title: spezi new fills the front matter
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_new.py:test_new_writes_a_spec_that_passes_the_check
implementation:
  - src/spezi/new.py
scope:
  - src/spezi/
---

# spezi new fills the front matter

`spezi new` must set `id`, `title`, `kind`, `owner`, `updated`, the `#` title and `scope` of the
new spec.

Reason: The new spec passes the check of the front matter (spec 000009).

Test: `tests/test_new.py`.
