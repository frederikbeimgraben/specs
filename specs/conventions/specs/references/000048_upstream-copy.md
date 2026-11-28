---
id: "000048"
title: The rules of a different repository are an unchanged copy
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_kit.py:test_a_copy_keeps_a_folder_named_upstream
implementation:
  - src/spezi/changes.py
  - src/spezi/check.py
  - src/spezi/kit.py
scope:
  - specs/
---

# The rules of a different repository are an unchanged copy

The rules of a different repository must be a copy of its `specs/` folder below
`specs/.upstream/<host>/<group>/.../<repo>/`. `ref` in `spezi.toml` must name a tag, a branch or
a commit, and `spezi.lock` must hold the commit of the copy (000082). When the table of the
repository in `spezi.toml` has `include`, the copy must hold only the folders below `specs/` that
`include` names, for example `include = ["style/python/"]`, and no other file. A folder of
`include` must be a path of kebab-case folder names below `specs/`.
The copy must not hold the hidden folders of the repository, for example `specs/.upstream/`.
The copy of a direct upstream must also hold the `spezi.lock` of the repository (000092).
When the repository uses an older kit, the copy must hold its rules after the migrations of
000081, and else no change. A person or an agent must not change a file of the copy. Only these
commands must change the copy, its `ref` and its entry in `spezi.lock`:

| Command | Effect |
| --- | --- |
| `spezi add <repo> [<ref>] [--include <folder>]...` | Adds the copy of a new repository (000068). |
| `spezi update [<repo> [<ref>]]` | Resolves the `ref` of one repository, or of each, again and replaces its copy (000067). |
| `spezi install` | Loads each copy again that does not agree with `spezi.lock`, and changes no `ref` and no commit (000083). |

Reason: The copy lets an agent and the check read the rules without a network. One `ref` makes
an update of the rules one diff in one pull request. With `include`, a project takes only the
rules that it needs, and an agent cannot read and follow the other rules.

Test: `spezi check` checks that each repository of `spezi.toml` has a copy, each copy has
a repository in `spezi.toml` or in a list `transitive` (000092), each folder of `include` is in the copy, the copy holds no file
outside the folders of `include` other than `spezi.lock` and the hash of the copy is the hash
in `spezi.lock`.
