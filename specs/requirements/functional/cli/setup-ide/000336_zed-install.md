---
id: "000336"
title: spezi setup-ide zed tells how to install the extension
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/ide.py
  - src/spezi/cli.py
  - src/spezi/kit.py
  - src/spezi/data/editors/
  - flake.nix
scope:
  - src/spezi/
  - flake.nix
---

# spezi setup-ide zed tells how to install the extension

For `zed`, `spezi setup-ide` must show that the Zed action `zed: install dev extension` with the
folder `.zed/spezi/` installs the extension. It also shows that Zed needs rustup to build it.

Reason: Zed has no command line to install an extension.

Test: Review.
