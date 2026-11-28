---
id: "000208"
title: The flake sets the version from the commit
kind: workflow
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - flake.nix
scope:
  - .github/workflows/release.yml
  - pyproject.toml
---

# The flake sets the version from the commit

The flake must set the version `0.0.0+<short commit>`.

Reason: The flake has no git history, so `setuptools-scm` cannot find a tag.

Test: `nix run . -- --version`.
