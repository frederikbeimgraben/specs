---
id: "000301"
title: spezi update tells to load the devShell again
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/devshell.py
scope:
  - src/spezi/
---

# spezi update tells to load the devShell again

When `spezi update` changed `flake.nix` in a devShell (`IN_NIX_SHELL`) without direnv, it must
tell to leave the shell and run `nix develop`.

Reason: A program cannot load its shell again.

Test: Review.
