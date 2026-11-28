---
id: "000305"
title: spezi add copies only the chosen folders
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_kit.py:test_add_with_include_copies_only_the_folders
implementation:
  - src/spezi/kit.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# spezi add copies only the chosen folders

The folders to copy can come from one or more `--include <folder>` or from the checklist
(spec 000085). Then `spezi add` must copy only these folders below `specs/`. It writes them as
`include` to the table (spec 000048).

Reason: A project takes only the rules that it needs.

Test: `tests/test_kit.py`.
