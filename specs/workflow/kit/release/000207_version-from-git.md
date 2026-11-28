---
id: "000207"
title: The version comes from the git tag
kind: workflow
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - pyproject.toml
scope:
  - .github/workflows/release.yml
  - pyproject.toml
---

# The version comes from the git tag

The version of the package must come from git with `setuptools-scm`. The tag `v1.2.3` gives the
version `1.2.3`.

Reason: The tag is the only place that sets a version.

Test: The job `pypi` publishes the version of the tag.
