---
id: "000219"
title: spezi check needs no network
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/agents.py
  - src/spezi/check.py
  - src/spezi/index.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# spezi check needs no network

`spezi check` must not use the network.

Reason: The check runs without network access and gives the same result each time.

Test: Review.
