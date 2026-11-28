---
id: "000005"
title: Folder names are lower case kebab case
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# Folder names are lower case kebab case

Folder names must use only `a` to `z`, `0` to `9` and `-`.

Reason: The folder names become part of the rule IDs, where `/` is the separator.

Test: `spezi check`: every area and topic folder matches `^[a-z0-9]+(-[a-z0-9]+)*$`.
