---
id: "000259"
title: spezi update keeps flake.nix when flake is off
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/project.py
  - src/spezi/install.py
  - src/spezi/kit.py
  - src/spezi/devshell.py
  - src/spezi/check.py
  - src/spezi/data/spezi.toml
scope:
  - src/spezi/
  - spezi.toml
---

# spezi update keeps flake.nix when flake is off

`spezi update` must not change `flake.nix` when the switch `flake` is off (spec 000084).

Reason: A project without the switch manages its flake alone.

Test: Review.
