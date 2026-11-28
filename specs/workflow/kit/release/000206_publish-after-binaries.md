---
id: "000206"
title: The release publishes only after each binary passes
kind: workflow
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - .github/workflows/release.yml
scope:
  - .github/workflows/release.yml
  - pyproject.toml
---

# The release publishes only after each binary passes

The jobs `pypi` and `github` (spec 000091) must start only after each `binary` job is correct.
When a test of a binary fails, the workflow must publish nothing.

Reason: A binary that does not start does not get out.

Test: `.github/workflows/release.yml`.
