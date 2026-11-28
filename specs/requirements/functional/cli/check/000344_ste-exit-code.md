---
id: "000344"
title: A warning does not change the exit code
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_ste.py:test_check_passes_with_only_warnings
implementation:
  - src/spezi/ste.py
  - src/spezi/check.py
  - src/spezi/data/ste/
scope:
  - src/spezi/
---

# A warning does not change the exit code

A warning (spec 000093) must not change the exit code of `spezi check` (spec 000217).

Reason: A project with old text must pass the check also after an update of the kit.

Test: `tests/test_ste.py`.
