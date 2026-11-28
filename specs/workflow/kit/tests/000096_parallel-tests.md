---
id: "000096"
title: The tests of the kit run in parallel
kind: workflow
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - pyproject.toml
  - flake.nix
scope:
  - tests/
  - pyproject.toml
  - flake.nix
---

# The tests of the kit run in parallel

The development shell of the kit must have `pytest-xdist`. The setting `addopts` in
`[tool.pytest.ini_options]` of `pyproject.toml` must have `-n auto`, so that each run of
`pytest` uses all processor cores. A test must not use a file or a folder that a different test
can change.

Reason: Each test starts the command in a new process. On one core, the tests need many minutes.

Test: Review: `pyproject.toml` and `flake.nix`. `nix develop -c pytest` shows each test as passed.
