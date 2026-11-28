---
id: "000334"
title: The editor folder goes to .gitignore
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_setup_ide.py:test_the_folder_goes_to_gitignore
  - tests/test_setup_ide.py:test_a_tracked_folder_stays_out_of_gitignore
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

# The editor folder goes to .gitignore

`spezi setup-ide` must add the folder (spec 000089) to `.gitignore`. It does not add it when git
tracks a file of the folder or when `.gitignore` holds the folder already.

Reason: `server.json` holds a path of one computer.

Test: `tests/test_setup_ide.py`.
