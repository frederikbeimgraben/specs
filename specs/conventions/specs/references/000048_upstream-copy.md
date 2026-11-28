---
id: "000048"
title: The rules of a different repository are an unchanged copy
kind: convention
status: draft
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_kit.py:test_a_copy_keeps_a_folder_named_upstream
  - tests/test_kit.py:test_init_leaves_out_the_own_folders_of_the_kit
  - tests/test_kit.py:test_add_copies_an_own_folder_that_include_names
  - tests/test_install.py:test_install_adds_the_line_to_gitattributes
  - tests/test_install.py:test_check_finds_a_missing_line_in_gitattributes
implementation:
  - src/spezi/changes.py
  - src/spezi/check.py
  - src/spezi/kit.py
  - src/spezi/install.py
scope:
  - specs/
---

# The rules of a different repository are an unchanged copy

The rules of a different repository must be a copy of its `specs/` folder below
`specs/.upstream/<host>/<group>/.../<repo>/`. `ref` in `spezi.toml` must name a tag, a branch or
a commit, and `spezi.lock` must hold the commit of the copy (spec 000082). When the table of the
repository in `spezi.toml` has `include`, the copy must hold only the folders below `specs/`
that `include` names, for example `include = ["style/python/"]`, and no other file. A folder of
`include` must be a path of kebab-case folder names below `specs/`. When the `spezi.toml` of the
repository has `own` (spec 000078), the copy must not hold the folders below `specs/` that `own`
names, for example `own = ["requirements/"]`. These folders hold the rules that apply only to
the repository itself. A folder of `own` that `include` names, or that holds a folder of
`include`, must be in the copy. The copy must not hold the hidden folders of the repository, for
example `specs/.upstream/`. The copy of a direct upstream must also hold the `spezi.lock` of the
repository (spec 000092). When the repository uses an older kit, the copy must hold its rules
after the migrations of (spec 000081), and else no change. A person or an agent must not change
a file of the copy. Only these commands must change the copy, its `ref` and its entry in
`spezi.lock`:

| Command | Effect |
| --- | --- |
| `spezi add <repo> [<ref>] [--include <folder>]...` | Adds the copy of a new repository (spec 000068). |
| `spezi update [<repo> [<ref>]]` | Resolves the `ref` of one repository, or of each, again and replaces its copy (spec 000067). |
| `spezi install` | Loads each copy again that does not agree with `spezi.lock`, and changes no `ref` and no commit (spec 000083). |

When `specs/.upstream/` holds a copy, `.gitattributes` in the root of the project must hold the
line `specs/.upstream/** -text`. `spezi install` must add this line when it is missing, and must
not change the other lines. A command must not remove the line.

Reason: The copy lets an agent and the check read the rules without a network. One `ref` makes
an update of the rules one diff in one pull request. With `include`, a project takes only the
rules that it needs, and an agent cannot read and follow the other rules. Git on Windows can
change the line ends of a file at checkout. The line in `.gitattributes` stops this, so the
copy keeps the bytes of its hash.

Test: `spezi check` checks these conditions:

- Each repository of `spezi.toml` has a copy.
- Each copy has a repository in `spezi.toml` or in a list `transitive` (spec 000092).
- Each folder of `include` is in the copy.
- The copy holds no file outside the folders of `include` other than `spezi.lock`.
- The hash of the copy is the hash in `spezi.lock`.

When `specs/.upstream/` holds a copy, it checks that `.gitattributes` holds
the line `specs/.upstream/** -text`.
