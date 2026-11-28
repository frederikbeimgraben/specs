---
id: "000309"
title: spezi remove keeps the other lines of spezi.toml
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/kit.py
  - src/spezi/cli.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# spezi remove keeps the other lines of spezi.toml

`spezi remove` must keep each line of `spezi.toml` outside the table of `<repo>`.

Reason: The other settings and the comments of a person stay.

Test: Review.
