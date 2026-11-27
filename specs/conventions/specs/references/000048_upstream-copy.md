---
id: "000048"
title: The rules of a different repository are an unchanged copy
kind: convention
status: approved
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
`.specs/upstream/<host>/<group>/.../<repo>/`. `ref` in `specs.toml` must name the commit of the
copy. When the table of the repository in `specs.toml` has `include`, the copy must hold only
the folders below `specs/` that `include` names, for example `include = ["style/python/"]`, and
no other file. A folder of `include` must be a path of kebab-case folder names below `specs/`.
A person or an agent must not change a file of the copy. Only these commands must change the
copy and its `ref`:

| Command | Effect |
| --- | --- |
| `specs add <repo> <ref> [--include <folder>]...` | Adds the copy of a new repository (000068). |
| `specs update <repo> <ref>` | Replaces the copy of one repository with its rules at `<ref>` (000067). |
| `specs update [<ref>]` | Does the same for the kit `github.com/frederikbeimgraben/specs`, and also replaces the templates, the skills, the CI file and the MCP server entry of the kit. Without `<ref>`, it takes the default branch. |

Reason: The copy lets an agent and the check read the rules without a network. One `ref` makes
an update of the rules one diff in one pull request. With `include`, a project takes only the
rules that it needs, and an agent cannot read and follow the other rules.

Test: `specs check` checks that each repository of `specs.toml` has a copy, each copy has
a repository in `specs.toml`, each folder of `include` is in the copy and the copy holds no file
outside the folders of `include`. A review checks that nobody changed the copy.
