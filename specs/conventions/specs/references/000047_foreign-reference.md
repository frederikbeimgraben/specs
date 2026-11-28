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
the full path of the repository, with each group and subgroup. A reference to a rule of the same
repository must be only the number. This is the short form:

| Rule | Short form | Long form |
| --- | --- | --- |
| Same repository | `000012` | `C/specs/format/000012` |
| Different repository | `github.com/frederikbeimgraben/spezi:000012` | `github.com/frederikbeimgraben/spezi:C/specs/format/000012` |

Code (spec 000017), the front matter (spec 000009) and the text of a spec must use the short form. A
reference in the text of a spec or in the code to a rule of the same repository must name a rule
of the project with the status `draft` or `approved`.
`spezi resolve <ID>` must print the long form of a short or a long form (spec 000070).
`spezi show <ID>` must print the full text of the rule (spec 000071).

Reason: Two repositories can use the same number. The host and the full path make the
reference unique. A GitLab project can be in subgroups, so the path can have more than two
parts. The number is the identity of a rule (spec 000013), so the short form stays
correct when a rule moves. The two commands give the kind, the path and the text without a
search by hand.

Test: `spezi check` finds each reference to a different repository, checks that it uses the
short form and checks that the rule exists in the copy of (spec 000048). It finds each number in the
text of a spec and each `§` reference in the code, and checks that it names a rule of the
project with the status `draft` or `approved`.
