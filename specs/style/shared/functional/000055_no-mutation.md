---
id: "000055"
title: A value is not mutated
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
implementation:
  - src/specs_kit/
scope:
  - src/
---

# A value is not mutated

Code must not change a value in place. It must build the new value whole.

Reason: A value that does not change cannot change behind the back of a different part of the
code.
