---
id: "000047"
title: A reference to a rule of a different repository names the repository
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# A reference to a rule of a different repository names the repository

A reference to a rule of a different repository must put the repository before the rule, in
the form `<host>/<group>/.../<repo>:<number>`. The path between the host and the colon must be
the full path of the repository, with each group and subgroup:

| Rule | Short form | Long form |
| --- | --- | --- |
| Same repository | `000012` | `C/specs/format/000012` |
| Different repository | `github.com/frederikbeimgraben/spezi:000012` | `github.com/frederikbeimgraben/spezi:C/specs/format/000012` |

Reason: Two repositories can use the same number. The host and the full path make the
reference unique. A GitLab project can be in subgroups, so the path can have more than two
parts.

Test: `spezi check` finds each reference to a different repository. It checks that the rule
exists in the copy (spec 000048).
