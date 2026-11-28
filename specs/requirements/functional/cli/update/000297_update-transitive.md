---
id: "000297"
title: spezi update follows the new lock of a direct upstream
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_transitive.py:test_update_with_recursive_adds_a_new_transitive_upstream
implementation:
  - src/spezi/kit.py
  - src/spezi/cli.py
  - src/spezi/devshell.py
scope:
  - src/spezi/
---

# spezi update follows the new lock of a direct upstream

`spezi update` must keep `transitive` and copy each of its repositories at the commit of the new
`spezi.lock` of the direct upstream (spec 000092).

| Case | Action |
| --- | --- |
| The new `spezi.lock` names a repository that `transitive` does not hold. | Ask (spec 000085). With `-r` (also `--recursive`), copy it without a question. |
| `transitive` holds a repository that the new `spezi.lock` does not name. | Remove it from `transitive`. Remove its copy when no other list `transitive` holds it. |

Reason: The transitive upstreams follow the version of their direct upstream.

Test: `tests/test_transitive.py`.
