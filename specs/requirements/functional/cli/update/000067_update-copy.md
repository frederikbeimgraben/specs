---
id: "000067"
title: specs update replaces a copy and its ref
kind: functional
status: draft
owner: frederikbeimgraben
updated: 2026-11-27
implementation:
  - src/specs_kit/kit.py
scope:
  - src/specs_kit/
---

# specs update replaces a copy and its ref

`specs update <repo> <ref>` must replace the copy of `<repo>` below `.specs/upstream/` with the
`specs/` folder of `<repo>` at `<ref>`, and set `ref` in `specs.toml` to the commit of `<ref>`.
`specs update [<ref>]` must do the same for the kit, and must also replace the templates, the
skills, the CI file and the entry `specs` in `.mcp.json`. Without `<ref>`, it must take the
default branch. The command must stop with an error when `<repo>` is not in `specs.toml`, or
when the kit at `<ref>` has no `.specs/templates/`. It must then change no file.

Reason: An update is one command and one diff (000048).
