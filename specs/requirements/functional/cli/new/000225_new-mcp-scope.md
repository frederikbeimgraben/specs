---
id: "000225"
title: The MCP tool new takes the scope as a list
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/new.py
scope:
  - src/spezi/
---

# The MCP tool new takes the scope as a list

The MCP tool `new` must take `scope` as a list of paths.

Reason: An agent gives each scope path as one item.

Test: Review.
