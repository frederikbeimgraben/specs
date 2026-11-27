---
id: "000048"
title: The rules of a different repository are an unchanged copy
kind: convention
status: draft
owner: frederikbeimgraben
updated: 2026-11-27
implementation:
  - src/specs_kit/check.py
  - src/specs_kit/kit.py
scope:
  - specs/
---

# The rules of a different repository are an unchanged copy

The rules of a different repository must be a copy of its `specs/` folder below
`specs/.upstream/<host>/<group>/.../<repo>/`. `ref` in `specs.toml` must name a tag, a branch or
a commit, and `specs.lock` must hold the commit of the copy (000082). When the table of the
repository in `specs.toml` has `include`, the copy must hold only the folders below `specs/` that
`include` names, for example `include = ["style/python/"]`, and no other file. A folder of `include` must be a path of kebab-case folder names below `specs/`.
The copy must not hold the hidden folders of the repository, for example `specs/.upstream/`.
When the repository uses an older kit, the copy must hold its rules after the migrations of
000081, and else no change. A person or an agent must not change a file of the copy. Only these
commands must change the copy, its `ref` and its entry in `specs.lock`:

| Command | Effect |
| --- | --- |
| `specs add <repo> [<ref>] [--include <folder>]...` | Adds the copy of a new repository (000068). |
| `specs update [<repo> [<ref>]]` | Resolves the `ref` of one repository, or of each, again and replaces its copy (000067). |
| `specs install` | Loads each copy again that does not agree with `specs.lock`, and changes no `ref` and no commit (000083). |

Reason: The copy lets an agent and the check read the rules without a network. One `ref` makes
an update of the rules one diff in one pull request. With `include`, a project takes only the
rules that it needs, and an agent cannot read and follow the other rules.

Test: `specs check` checks that each repository of `specs.toml` has a copy, each copy has
a repository in `specs.toml`, each folder of `include` is in the copy, the copy holds no file
outside the folders of `include` and the hash of the copy is the hash in `specs.lock`.
