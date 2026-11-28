---
id: "000302"
title: spezi update stops in four cases
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_kit.py:test_update_stops_for_an_unknown_repository
implementation:
  - src/spezi/kit.py
  - src/spezi/cli.py
  - src/spezi/devshell.py
scope:
  - src/spezi/
---

# spezi update stops in four cases

`spezi update` must stop with an error in these cases:

- `<repo>` is not in `spezi.toml`.
- `<repo>` at `<ref>` has no folder of `include`.
- The kit at `<ref>` has no `specs/.templates/`.
- The switch `ci` is on and `.gitlab-ci.yml` has an `include` that is not a list.

It then changes no file of the repository with the error.

Reason: A broken version never replaces a copy.

Test: `tests/test_kit.py`.
