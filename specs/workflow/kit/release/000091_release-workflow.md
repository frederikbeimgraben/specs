---
id: "000091"
title: A tag publishes the package and the binaries
kind: workflow
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - .github/workflows/release.yml
  - pyproject.toml
  - flake.nix
  - src/spezi/ide.py
scope:
  - .github/workflows/release.yml
  - pyproject.toml
---

# A tag publishes the package and the binaries

The kit must have a CI workflow `release.yml`. A push of a tag `v*` must publish a release with
these jobs:

| Job | What it does |
| --- | --- |
| `vsix` | It builds the `.vsix` of the VS Code extension with `nix build .#vsix`. |
| `binary` | It builds one file `spezi` with PyInstaller `--onefile`, with the package data and the `.vsix`, for `linux-x86_64` on `ubuntu-latest`, `linux-arm64` on `ubuntu-24.04-arm` and `windows-x86_64` on `windows-latest`. Then it runs `spezi --help` and `spezi check` in the kit. |
| `pypi` | Only for a tag: it builds the sdist and the wheel of `spezi-kit` and publishes them to PyPI with Trusted Publishing, in the environment `release`. |
| `github` | Only for a tag: it makes a GitHub release with the binaries and with the release notes that GitHub makes from the merged pull requests. |

Reason: A release needs no manual step.

Test: The workflow `release.yml` builds and tests the binaries on each pull request.
