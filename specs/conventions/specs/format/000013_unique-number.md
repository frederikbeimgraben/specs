---
id: "000013"
title: The number is the identity of a rule
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
  - spezi.toml
scope:
  - specs/
---

# The number is the identity of a rule

The number must be unique over all specs of the repository. The rules of a different
repository keep their numbers (spec 000047). The number is the real ID. Kind and path only make
the ID readable. A new rule must get the highest number plus one, counted over the base branch
and every open pull request. When two pull requests hold the same number, the pull request that
merges later must give its spezi new numbers before its merge. A number must never be used
again.

`base_ref` in `spezi.toml` names the base branch, for example `origin/main`.

Reason: An old reference must not point to a different rule, also after a file moves.

Test: `spezi check`: no number occurs two times. No spec of a branch has a number that the base
branch gave to a different spec after the branch left it.
