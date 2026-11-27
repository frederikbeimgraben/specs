---
id: "000071"
title: specs show prints the full text of a spec
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
implementation:
  - src/specs_kit/queries.py
scope:
  - src/specs_kit/
---

# specs show prints the full text of a spec

`specs show <id>` must print the full text of the spec file for a short or a long form of
000047. It must stop with an error when no rule of the project or of a copy has this ID.

Reason: An agent reads a rule of a copy with the same command as a rule of the project.
