---
id: "000339"
title: ste = false turns off the check of ASD-STE100
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_ste.py:test_check_without_ste
implementation:
  - src/spezi/ste.py
  - src/spezi/check.py
  - src/spezi/data/ste/
scope:
  - src/spezi/
---

# ste = false turns off the check of ASD-STE100

With `ste = false` in `spezi.toml` (spec 000078), `spezi check` must not check ASD-STE100
(spec 000093).

Reason: A project in a different language can turn off the check.

Test: `tests/test_ste.py`.
