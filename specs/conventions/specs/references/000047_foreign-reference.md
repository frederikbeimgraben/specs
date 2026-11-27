---
id: "000047"
title: A reference to a rule of a different repository names the repository
kind: convention
status: draft
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - src/specs_kit/check.py
scope:
  - specs/
---

# A reference to a rule of a different repository names the repository

A reference to a rule of a different repository must put the repository before the rule, in
the form `<host>/<owner>/<repo>:<number>`. A reference to a rule of the same repository must
be only the number. This is the short form:

| Rule | Short form | Long form |
| --- | --- | --- |
| Same repository | `000012` | `C/specs/format/000012` |
| Different repository | `github.com/frederikbeimgraben/specs:000012` | `github.com/frederikbeimgraben/specs:C/specs/format/000012` |

Code (000017), the front matter (000009) and the text of a spec must use the short form.
`specs resolve <ID>` must print the long form of a short or a long form. `specs show <ID>` must
print the full text of the rule.

Reason: Two repositories can use the same number. The host, the owner and the repository make
the reference unique. The number is the identity of a rule (000013), so the short form stays
correct when a rule moves. The two commands give the kind, the path and the text without a
search by hand.

Test: `specs check` finds each reference to a different repository, checks that it uses the
short form and checks that the rule exists in the copy of 000048.
