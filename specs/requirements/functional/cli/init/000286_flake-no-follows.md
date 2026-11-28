---
id: "000286"
title: The input spezi does not follow nixpkgs
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/kit.py
  - src/spezi/devshell.py
  - src/spezi/cli.py
  - src/spezi/install.py
  - src/spezi/data/
scope:
  - src/spezi/
---

# The input spezi does not follow nixpkgs

The input `spezi` of `flake.nix` must not follow the input `nixpkgs` of the project.

Reason: The program then builds with the `nixpkgs` that the kit tested.

Test: Review.
