---
id: "000288"
title: spezi init stops in five cases
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_kit.py:test_init_stops_when_the_kit_is_there
implementation:
  - src/spezi/kit.py
  - src/spezi/devshell.py
  - src/spezi/cli.py
  - src/spezi/install.py
  - src/spezi/data/
scope:
  - src/spezi/
---

# spezi init stops in five cases

`spezi init` must stop with an error and change no file in these cases:

- `spezi.toml` exists.
- The forge is unknown.
- The switch `ci` is on and `.gitlab-ci.yml` has an `include` that is not a list.
- `<dir>` is the kit.
- This program is an older commit of the kit than the commit of the `ref`.

Reason: The command never writes over a project that has the kit.

Test: `tests/test_kit.py`.
