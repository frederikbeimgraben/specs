---
id: "000296"
title: spezi update gives one line for each transitive upstream
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_transitive.py:test_update_lists_a_transitive_upstream_with_a_new_commit
implementation:
  - src/spezi/kit.py
  - src/spezi/cli.py
  - src/spezi/devshell.py
scope:
  - src/spezi/
---

# spezi update gives one line for each transitive upstream

Below its message, `spezi update` must give one line for each transitive upstream
(spec 000092), sorted by repository. These are the hints of `spezi install`
(spec 000289). For a transitive upstream whose commit did not change, the line is
`<repo> is up to date at <commit> via <direct>`. `<direct>` is the list `via` of `spezi.lock`
(spec 000082), separated by `, `.

Reason: The person sees each transitive upstream, also when it did not change.

Test: `tests/test_transitive.py`.
