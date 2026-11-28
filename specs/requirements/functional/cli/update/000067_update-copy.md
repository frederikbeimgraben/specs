---
id: "000067"
title: spezi update resolves the refs again and replaces the copies
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_kit.py:test_update_replaces_the_copy_and_keeps_include
  - tests/test_kit.py:test_update_of_the_kit_runs_the_check
  - tests/test_kit.py:test_update_without_arguments_updates_each_repository
  - tests/test_kit.py:test_update_reads_a_ref_without_spaces
implementation:
  - src/spezi/kit.py
  - src/spezi/cli.py
  - src/spezi/devshell.py
scope:
  - src/spezi/
---

# spezi update resolves the refs again and replaces the copies

`spezi update [<repo> [<ref>]] [-y] [-r]` must update the copies below `specs/.upstream/`
(spec 000048), after the questions (spec 000085):

| Form | Effect |
| --- | --- |
| `spezi update` | Resolves the `ref` of each repository of `spezi.toml` again. |
| `spezi update <repo>` | Resolves the `ref` of `<repo>` again. |
| `spezi update <repo> <ref>` | Sets `ref` of `<repo>` in `spezi.toml` to `<ref>` as given, a tag, a branch or a commit, and resolves it. |

`<repo>` is the full name of the repository, or `kit` for `github.com/frederikbeimgraben/spezi`.
For each repository, the command must replace the copy with the `specs/` folder at the commit
that `ref` names. It writes the `ref`, the commit, `include` and the hash to `spezi.lock`
(spec 000082). The kit comes first.

Reason: `spezi.toml` keeps the version that the project wants, and one command takes the newest
commit of each version (spec 000048).

Test: `tests/test_kit.py`.
