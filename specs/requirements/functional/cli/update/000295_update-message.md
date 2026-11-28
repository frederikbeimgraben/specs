---
id: "000295"
title: spezi update gives one line for each repository
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_transitive.py:test_update_without_a_new_commit_changes_no_file
implementation:
  - src/spezi/kit.py
  - src/spezi/cli.py
  - src/spezi/devshell.py
scope:
  - src/spezi/
---

# spezi update gives one line for each repository

The message of `spezi update` must have one line for each repository, in the order of the
update:

| Case | Line |
| --- | --- |
| The new commit is the commit of `<repo>` in `spezi.lock` before the command. | `<repo> is up to date at <commit>` |
| Else | `updated <repo> to <commit>` |

Reason: The person sees which repository changed.

Test: `tests/test_transitive.py`.
