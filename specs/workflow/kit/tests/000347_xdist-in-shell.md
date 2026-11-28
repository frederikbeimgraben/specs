---
id: "000347"
title: The development shell has pytest-xdist
kind: workflow
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - flake.nix
scope:
  - tests/
  - pyproject.toml
  - flake.nix
---

# The development shell has pytest-xdist

The development shell of the kit must have `pytest-xdist`.

Reason: `-n auto` (spec 000096) needs this plugin.

Test: Review: `flake.nix`.
