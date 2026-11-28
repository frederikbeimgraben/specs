---
id: "000068"
title: spezi add adds the copy of a different repository
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_kit.py:test_add_copies_the_rules
  - tests/test_kit.py:test_add_with_include_copies_only_the_folders
  - tests/test_kit.py:test_add_stops_for_a_repository_in_the_settings
  - tests/test_kit.py:test_add_without_ref_takes_the_default_branch
  - tests/test_transitive.py:test_add_with_recursive_copies_the_transitive_upstream
  - tests/test_transitive.py:test_add_without_recursive_copies_no_transitive_upstream
implementation:
  - src/spezi/kit.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# spezi add adds the copy of a different repository

`spezi add [<repo> [<ref>]] [-y] [-r]` must ask the questions (spec 000085), and must then copy the
`specs/` folder of `<repo>` at `<ref>` to `specs/.upstream/<repo>/`, add `[upstream."<repo>"]`
with `<ref>` as given as `ref` to `spezi.toml`, and write the entry of `<repo>` to `spezi.lock`
(spec 000082). Without `<ref>`, the command must take or propose the tag with the highest version,
for example `v1.10` before `v1.9`. A tag has a version when it has the form `1.2.3` or `v1.2.3`
with one or more numbers. Without such a tag, it must take the name of the default branch.
`<repo>` must have the form `<host>/<group>/.../<repo>` with one or more groups. With one or
more `--include <folder>`, or with the folders of the checklist (spec 000085), the command must copy
only these folders below `specs/` and must write them as `include` to the table (spec 000048). A
folder below a different folder of `include` must not go to `include`. The command must stop
with an error and change no file when `<repo>` is in `spezi.toml` already, or when `<repo>` at
`<ref>` has no folder of `--include`.

The command must then copy the transitive upstreams (spec 000092) that the user chooses (spec 000085), and
write them as `transitive` to the table. With `-r` (also `--recursive`), it must copy each
transitive upstream without a question.

Before it copies, the command must run the migrations (spec 000081). It must stop with an error when
this program is an older commit of the kit than the kit commit in `spezi.lock`.

At its end, the command must do the steps of `spezi install` (spec 000083).

Reason: A project takes the rules of a different repository, or only the rules that it needs,
with one command (spec 000048). With `-r`, a script copies the rules that the rules of `<repo>`
refer to, without a question. The new rules can show errors in the project, and the index must
show them.

Test: `tests/test_kit.py`.
