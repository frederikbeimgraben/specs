---
id: "000307"
title: spezi add stops for a known repository or a missing folder
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_kit.py:test_add_stops_for_a_repository_in_the_settings
implementation:
  - src/spezi/kit.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# spezi add stops for a known repository or a missing folder

`spezi add` must stop with an error and change no file in these cases:

- `<repo>` is in `spezi.toml` already.
- `<repo>` at `<ref>` has no folder of `--include`.

Reason: A second table for one repository gives two copies.

Test: `tests/test_kit.py`.
