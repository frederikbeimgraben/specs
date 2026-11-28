---
id: "000285"
title: The flake input spezi names the commit of the lock
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/kit.py
  - src/spezi/devshell.py
  - src/spezi/cli.py
  - src/spezi/install.py
  - src/spezi/data/
scope:
  - src/spezi/
---

# The flake input spezi names the commit of the lock

The input of the kit in `flake.nix` must be the line
`inputs.spezi.url = "github:frederikbeimgraben/spezi/<commit>";`, with the commit of
`spezi.lock`. The line must be below the comment
`# The spezi command of the kit. The ref must be the commit in spezi.lock.`.

Reason: The program of the devShell is the kit of the copy.

Test: `tests/test_kit.py`.
