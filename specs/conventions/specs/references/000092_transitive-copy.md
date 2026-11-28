---
id: "000092"
title: A copy brings the upstreams of its repository
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_transitive.py:test_add_with_recursive_copies_the_transitive_upstream
  - tests/test_transitive.py:test_the_project_itself_gets_no_copy
  - tests/test_transitive.py:test_two_commits_of_one_upstream_are_an_error
  - tests/test_transitive.py:test_union_of_folders
implementation:
  - src/spezi/transitive.py
  - src/spezi/kit.py
  - src/spezi/check.py
scope:
  - specs/
  - spezi.toml
---

# A copy brings the upstreams of its repository

A direct upstream is a repository with a table `[upstream."<repo>"]` in `spezi.toml`. Its
`spezi.lock` names its own upstreams, direct and transitive. These are the transitive upstreams
of the project. The list `transitive` in the table of the direct upstream must name each
transitive upstream that the project copies:

```toml
repo = "github.com/frederikbeimgraben/spezi"

[upstream."github.com/frederikbeimgraben/spezi-python"]
ref = "v1.0"
transitive = ["github.com/example/other"]
```

For each repository of `transitive`, these rules apply:

| Case | Effect |
| --- | --- |
| The repository is `repo` of `spezi.toml`, the project itself. | No copy. |
| The repository has its own table in `spezi.toml`. | No copy from `transitive`. The direct table wins. |
| Else | A copy below `specs/.upstream/<repo>/` (000048), at the `commit` that the `spezi.lock` of the direct upstream names for it, with its `include` from that entry. |

The copy of each direct upstream must hold its `spezi.lock` as `specs/.upstream/<repo>/spezi.lock`,
unchanged. The copy of a transitive upstream must not hold a `spezi.lock`.

When two direct upstreams name the same transitive upstream with the same commit, the copy must
hold the union of the two `include` lists. An empty `include` is all rules. When they name
different commits, `spezi check` must show an error that names the repository and both direct
upstreams. A table for the repository in `spezi.toml` of the project removes the error.

A copy of a transitive upstream follows 000048 and 000049 like a copy of a direct upstream.
Only `spezi init`, `spezi add` and `spezi update` must change `transitive` (000085).

Reason: A rule of an upstream can refer to a rule of its own upstream. The copy of that
upstream makes the reference readable without a network. The commit of the upstream's
`spezi.lock` is the commit that the upstream checked its rules against. `repo` stops a cycle,
for example when two repositories copy the rules of each other. The copy of `spezi.lock` lets
the check find a conflict without a network. A conflict of two commits needs a decision of a person.

Test: `spezi check` checks that each repository of `transitive` has a copy or is skipped by the
table above, that the commit and the `include` of each copy agree with the `spezi.lock` of its
direct upstreams in their `specs/.upstream/<repo>/spezi.lock`, and that no two direct upstreams
name different commits. The check uses no network.
