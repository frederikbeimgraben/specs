---
id: "000348"
title: A test uses only its own files
kind: workflow
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - tests/
scope:
  - tests/
  - pyproject.toml
  - flake.nix
---

# A test uses only its own files

A test of the kit must not use a file or a folder that a different test can change.

Reason: Tests that run in parallel (spec 000096) otherwise change the files of each other.

Test: `nix develop -c pytest` passes in each order.
