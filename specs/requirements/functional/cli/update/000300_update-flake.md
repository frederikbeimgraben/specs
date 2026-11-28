---
id: "000300"
title: spezi update sets the flake input to the new commit
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/devshell.py
scope:
  - src/spezi/
---

# spezi update sets the flake input to the new commit

When `flake.nix` has the input `spezi` (spec 000285), `spezi update` of the kit must set
its ref to the new commit of the kit. It must then run `nix flake update spezi`. Without this
input, it must not change `flake.nix` and `flake.lock`.

Reason: The program of the devShell stays the kit of the copy.

Test: Review.
