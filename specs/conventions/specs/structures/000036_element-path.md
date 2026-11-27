---
id: "000036"
title: An element names the code that holds it
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - src/specs_kit/check.py
  - src/specs_kit/sections.py
scope:
  - specs/
---

# An element names the code that holds it

`Path` must be the file or the folder that holds the element, as a path from the repository
root. The path must exist. An element without code, for example an external system, must have
`-` as its path. A structure spec with an element path must list the same paths, or their
folders, in `implementation`.

Reason: A reader goes from the diagram to the code in one step. A moved file breaks the check,
so the diagram cannot point to old code.

Test: `specs check` checks that each path exists. A review checks `implementation`.
