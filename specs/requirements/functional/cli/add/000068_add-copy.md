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
  - tests/test_kit.py:test_add_without_ref_takes_the_default_branch
implementation:
  - src/specs_kit/kit.py
  - src/specs_kit/cli.py
scope:
  - src/specs_kit/
---

# specs add adds the copy of a different repository

`specs add [<repo> [<ref>]] [-y]` must ask the questions of 000085, and must then copy the
`specs/` folder of `<repo>` at `<ref>` to `specs/.upstream/<repo>/`, add `[upstream."<repo>"]`
with `<ref>` as given as `ref` to `specs.toml`, and write the entry of `<repo>` to `specs.lock`
(000082). Without `<ref>`, the command must take or propose the tag with the highest version,
for example `v1.10` before `v1.9`. A tag has a version when it has the form `1.2.3` or `v1.2.3`
with one or more numbers. Without such a tag, it must take the name of the default branch.
`<repo>` must have the form `<host>/<group>/.../<repo>` with one or more groups. With one or
more `--include <folder>`, or with the folders of the checklist of 000085, the command must copy
only these folders below `specs/` and must write them as `include` to the table (000048). A
folder below a different folder of `include` must not go to `include`. The command must stop
with an error and change no file when `<repo>` is in `specs.toml` already, or when `<repo>` at
`<ref>` has no folder of `--include`.

Before it copies, the command must run the migrations of 000081. It must stop with an error when
this program is an older commit of the kit than the kit commit in `specs.lock`.

At its end, the command must do the steps of `specs install` (000083).

Reason: A project takes the rules of a different repository, or only the rules that it needs,
with one command (000048). The new rules can show errors in the project, and the index must
show them.

Test: `tests/test_kit.py`.
