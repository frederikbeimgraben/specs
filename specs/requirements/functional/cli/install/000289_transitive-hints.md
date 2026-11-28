---
id: "000289"
title: spezi install tells each new and each changed transitive upstream
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_transitive.py:test_install_restores_a_transitive_copy
implementation:
  - src/spezi/install.py
  - src/spezi/kit.py
  - src/spezi/cli.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# spezi install tells each new and each changed transitive upstream

`spezi install` must give a hint for each transitive upstream that step 4 (spec 000083) loads:

| Case | Hint |
| --- | --- |
| The upstream had no entry in `spezi.lock` before. | `installed <repo> at <commit> via <direct>` |
| The commit of the upstream changed. | `updated <repo> to <commit> via <direct>` |

`<direct>` is the list `via` of `spezi.lock` (spec 000082), separated by `, `. These hints come
first, sorted by repository.

Reason: The person sees each transitive upstream that changed.

Test: `tests/test_transitive.py`.
