---
id: "000243"
title: Each write of a file goes to the list
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/changes.py
  - src/spezi/cli.py
  - src/spezi/view.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# Each write of a file goes to the list

Each place in the code that writes a file must record it for the list of changed files
(spec 000077). A file that a different program writes for the command must be in the list too,
for example `flake.lock` from `nix flake lock`.

Reason: The list shows each change, also a change that a tool makes.

Test: Review.
