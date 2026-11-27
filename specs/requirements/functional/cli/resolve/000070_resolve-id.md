---
id: "000070"
title: specs resolve prints the long form of an ID
kind: functional
status: draft
owner: frederikbeimgraben
updated: 2026-11-27
implementation:
  - src/specs_kit/queries.py
  - src/specs_kit/project.py
scope:
  - src/specs_kit/
---

# specs resolve prints the long form of an ID

`specs resolve <id>` must print the long form of 000047 for a short or a long form, for
example `C/specs/format/000012` for `000012`. It must stop with an error when no rule of the
project or of a copy has this ID.

Reason: An agent gets the kind and the place of a rule without a search.
