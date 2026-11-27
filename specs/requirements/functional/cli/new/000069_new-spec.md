---
id: "000069"
title: specs new makes a new spec from its template
kind: functional
status: draft
owner: frederikbeimgraben
updated: 2026-11-27
implementation:
  - src/specs_kit/new.py
scope:
  - src/specs_kit/
---

# specs new makes a new spec from its template

`specs new <kind> <area>/<topic> <name> "<title>" --scope <path>... [--owner <login>]` must
copy the template of `<kind>` from `.specs/templates/` to
`specs/<kind folder>/<area>/<topic>/<number>_<name>.md` and print the path. `<kind>` is the kind
or its letter (000004). The number must be the highest number of `specs/` and of `base_ref` plus
one (000013). The command must set `id`, `title`, `kind`, `owner`, `updated`, the `#` title and
`scope`. `--scope` is required, one time for each path, and each path must exist. The owner must
come from `--owner`, else from `git config <forge>.user`. Without a scope, with a scope path that
does not exist, or without an owner, the command must stop with an error and write no file. For
a protocol with a JSON media type, the command must also write a minimal JSON Schema next to the
spec (000028). The MCP tool `new` must take `scope` as a list of paths.

Reason: A new spec starts correct, with the next free number (000008).
