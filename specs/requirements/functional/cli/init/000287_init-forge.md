---
id: "000287"
title: spezi init proposes the forge of the remote
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_kit.py:test_init_takes_the_forge_from_the_remote
  - tests/test_kit.py:test_init_reads_the_forge_from_the_host_only
implementation:
  - src/spezi/kit.py
  - src/spezi/devshell.py
  - src/spezi/cli.py
  - src/spezi/install.py
  - src/spezi/data/
scope:
  - src/spezi/
---

# spezi init proposes the forge of the remote

Without `--forge`, `spezi init` must propose the forge of `git remote origin` (spec 000085). It
reads the forge from the host of the URL only.

Reason: Most projects use the forge of their remote.

Test: `tests/test_kit.py`.
