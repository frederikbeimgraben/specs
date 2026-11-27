---
id: "000068"
title: specs add adds the copy of a different repository
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
implementation:
  - src/specs_kit/kit.py
scope:
  - src/specs_kit/
---

# specs add adds the copy of a different repository

`specs add <repo> <ref>` must copy the `specs/` folder of `<repo>` at `<ref>` to
`.specs/upstream/<repo>/` and add `[upstream."<repo>"]` with the commit as `ref` to
`specs.toml`. `<repo>` must have the form `<host>/<owner>/<repo>`. The command must stop with an
error when `<repo>` is in `specs.toml` already.

Reason: A project takes the rules of a different repository with one command (000048).
