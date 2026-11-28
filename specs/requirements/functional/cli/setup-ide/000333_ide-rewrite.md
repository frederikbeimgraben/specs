---
id: "000333"
title: spezi setup-ide writes the whole folder again
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/ide.py
  - src/spezi/cli.py
  - src/spezi/kit.py
  - src/spezi/data/editors/
  - flake.nix
scope:
  - src/spezi/
  - flake.nix
---

# spezi setup-ide writes the whole folder again

`spezi setup-ide` must write the whole folder (spec 000089) again when it exists.

Reason: A file of an older version does not stay.

Test: `tests/test_setup_ide.py`.
