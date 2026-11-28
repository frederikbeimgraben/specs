---
id: "000022"
title: A function body holds no comment
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# A function body holds no comment

A function body must not hold a `#` comment. A `# noqa` comment of (spec 000030) is the only
exception. A reason or a note goes into the docstring.

Reason: One place for the documentation. Tools show a docstring, but not a comment in the body.

Test: A review finds a comment in a body.
