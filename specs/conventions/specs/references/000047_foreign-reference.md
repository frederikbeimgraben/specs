---
id: "000047"
title: A reference to a rule of a different repository names the repository
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - scripts/check_specs.py
scope:
  - specs/
---

# A reference to a rule of a different repository names the repository

A reference to a rule of a different repository must put the repository before the rule ID, in
the form `<host>/<owner>/<repo>:<ID>`. Example: `github.com/frederikbeimgraben/specs:C/specs/format/000012`.
A reference to a rule of the same repository must not have this part. Code puts `§` before the
whole reference (000017).

Reason: Two repositories can use the same number. The host, the owner and the repository make
the reference unique.

Test: `scripts/check_specs.py` finds each reference to a different repository and checks that
the rule exists in the copy of 000048.
