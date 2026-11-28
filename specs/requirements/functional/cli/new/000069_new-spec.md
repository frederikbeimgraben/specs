---
id: "000069"
title: spezi new makes a new spec from its template
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/new.py
scope:
  - src/spezi/
---

# spezi new makes a new spec from its template

`spezi new <kind> <area>/<topic> <name> "<title>" --scope <path>... [--owner <login>]` must copy
the template of `<kind>` from `specs/.templates/` to
`specs/<kind folder>/<area>/<topic>/<number>_<name>.md` and print the path. `<kind>` is the kind
or its letter (spec 000004).

Reason: A new spec starts correct (spec 000008).

Test: `tests/test_new.py`.
