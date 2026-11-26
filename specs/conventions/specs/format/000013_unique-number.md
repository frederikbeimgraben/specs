---
id: "000013"
title: The number is the identity of a rule
kind: convention
status: draft
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - scripts/check_specs.py
  - specs/config.toml
scope:
  - specs/
---

# The number is the identity of a rule

The number must be unique over all specs. The number is the real ID. Kind and path only make
the ID readable. A new rule must get the highest number plus one, counted over the base branch
and every open pull request. When two pull requests hold the same number, the pull request that
merges later must give its specs new numbers before its merge. A number must never be used
again.

`base_ref` in `specs/config.toml` names the base branch, for example `origin/main`.

Reason: An old reference must not point to a different rule, also after a file moves.

Test: `scripts/check_specs.py`: no number occurs two times, and no spec of a branch has a number
that the base branch gave to a different spec after the branch left it.
