---
id: "000030"
title: A breaking change of a format is a new protocol spec
kind: convention
status: draft
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - scripts/check_specs.py
scope:
  - specs/
---

# A breaking change of a format is a new protocol spec

`version` must be a whole number from 1. A compatible change must change the spec in place and
must keep `version`. A breaking change must be a new protocol spec with a new number and
`version` plus one. The old spec must get `status: replaced` when the product no longer sends
or reads the old format.

Only these changes are compatible:

- A new optional key in an object.
- A new value in a list of values, if `## Compatibility` tells the receiver to ignore an
  unknown value.

All other changes are breaking changes.

Reason: A receiver that names the ID of a format must find the same contract later.

Test: Review. `scripts/check_specs.py` checks the form of `version`.
