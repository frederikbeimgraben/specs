---
id: "000048"
title: The rules of a different repository are an unchanged copy
kind: convention
status: draft
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - src/specs_kit/check.py
scope:
  - specs/
---

# The rules of a different repository are an unchanged copy

The rules of a different repository must be a copy of its `specs/` folder below
`.specs/upstream/<host>/<owner>/<repo>/`. `ref` in `specs.toml` must name the commit of the
copy. A person or an agent must not change a file of the copy. Only these commands must
change the copy and its `ref`:

| Command | Effect |
| --- | --- |
| `specs add <repo> <ref>` | Adds the copy of a new repository. |
| `specs update <repo> <ref>` | Replaces the copy of one repository with its rules at `<ref>`. |
| `specs update [<ref>]` | Does the same for the kit `github.com/frederikbeimgraben/specs`, and also replaces the templates, the skills, the CI file and the MCP server entry of the kit. Without `<ref>`, it takes the default branch. |

Reason: The copy lets an agent and the check read the rules without a network. One `ref` makes
an update of the rules one diff in one pull request.

Test: `specs check` checks that each repository of `specs.toml` has a copy and each copy has
a repository in `specs.toml`. A review checks that nobody changed the copy.
