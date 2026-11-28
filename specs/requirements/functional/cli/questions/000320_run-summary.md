---
id: "000320"
title: The summary shows the answers or the changed rules
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/ask.py
  - src/spezi/kit.py
  - src/spezi/review.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# The summary shows the answers or the changed rules

The summary before `Run?` (spec 000319) must show:

| Command | Summary |
| --- | --- |
| `spezi init` | The answers. |
| `spezi add`, `spezi update` | The old and the new `ref`, the new commit, and each new, changed and removed rule as `A`, `M` or `D` with its number and its title. |

Reason: The person sees which rules change before they change.

Test: Review.
