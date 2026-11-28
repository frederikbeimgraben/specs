---
id: "000205"
title: A pull request builds and tests the release
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

# A pull request builds and tests the release

Each pull request must run the release workflow (spec 000091) without the jobs `pypi` and
`github`.

Reason: A pull request shows that the release builds, and it publishes nothing.

Test: `.github/workflows/release.yml`.
