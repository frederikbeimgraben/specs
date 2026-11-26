---
id: "000048"
title: The rules of a different repository are an unchanged copy
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - scripts/check_specs.py
scope:
  - specs/
---

# The rules of a different repository are an unchanged copy

The rules of a different repository must be a copy of its `specs/` folder below
`specs/upstream/<host>/<owner>/<repo>/`. `ref` in `specs/config.toml` must name the tag or the
commit of the copy. A person or an agent must not change a file of the copy. An update must
replace the whole folder with `python3 scripts/check_specs.py --fetch`.

Reason: The copy lets an agent and the check read the rules without a network. One `ref` makes
an update of the rules one diff in one pull request.

Test: `scripts/check_specs.py` checks that each repository of `specs/config.toml` has a copy
and each copy has a repository in `specs/config.toml`. A review checks that nobody changed the
copy.
