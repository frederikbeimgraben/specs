---
id: "000068"
title: specs add adds the copy of a different repository
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
implementation:
  - src/specs_kit/kit.py
  - src/specs_kit/cli.py
scope:
  - src/specs_kit/
---

# specs add adds the copy of a different repository

`specs add <repo> <ref>` must copy the `specs/` folder of `<repo>` at `<ref>` to
`.specs/upstream/<repo>/` and add `[upstream."<repo>"]` with the commit as `ref` to
`specs.toml`. `<repo>` must have the form `<host>/<group>/.../<repo>` with one or more groups.
With one or more `--include <folder>`, the command must copy only these folders below `specs/`
and must write them as `include` to the table (000048). The command must stop with an error
and change no file when `<repo>` is in `specs.toml` already, or when `<repo>` at `<ref>` has no
folder of `--include`.

At its end, `specs add` must run `specs check --write` (000065) and print its report after its
own message. It must end with the exit code 1 when the check finds errors.

Reason: A project takes the rules of a different repository, or only the rules that it needs,
with one command (000048). The new rules can show errors in the project, and the index must
show them.
