---
id: "000291"
title: spezi install of a current project needs no network
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/install.py
  - src/spezi/kit.py
  - src/spezi/cli.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# spezi install of a current project needs no network

When each copy agrees with `spezi.lock` and this program is the kit at the commit of
`spezi.lock`, `spezi install` must not use the network.

Reason: A fresh clone of a current project installs without network access.

Test: `tests/test_install.py`.
