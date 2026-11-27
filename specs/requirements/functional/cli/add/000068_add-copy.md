---
id: "000068"
title: specs add adds the copy of a different repository
kind: functional
status: draft
owner: frederikbeimgraben
updated: 2026-11-27
tests:
  - tests/test_kit.py:test_add_copies_the_rules
  - tests/test_kit.py:test_add_with_include_copies_only_the_folders
  - tests/test_kit.py:test_add_stops_for_a_repository_in_the_settings
implementation:
  - src/specs_kit/kit.py
  - src/specs_kit/cli.py
scope:
  - src/specs_kit/
---

# specs add adds the copy of a different repository

`specs add <repo> <ref>` must copy the `specs/` folder of `<repo>` at `<ref>` to
`specs/.upstream/<repo>/` and add `[upstream."<repo>"]` with the commit as `ref` to
`specs.toml`. `<repo>` must have the form `<host>/<group>/.../<repo>` with one or more groups.
With one or more `--include <folder>`, the command must copy only these folders below `specs/`
and must write them as `include` to the table (000048). The command must stop with an error
and change no file when `<repo>` is in `specs.toml` already, or when `<repo>` at `<ref>` has no
folder of `--include`.

Before it copies, the command must run the migrations of 000081.

At its end, `specs add` must run `specs check --write` (000065) and print its report after its
own message. It must end with the exit code 1 when the check finds errors.

Reason: A project takes the rules of a different repository, or only the rules that it needs,
with one command (000048). The new rules can show errors in the project, and the index must
show them.

Test: `tests/test_kit.py`.
