---
id: "000006"
title: A rule is written in one place
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - specs/
scope:
  - specs/
---

# A rule is written in one place

A rule must be in the topic folder that it controls. A rule that applies to two areas must be in
the area that owns the code. A rule must not be written two times. A different spec must refer
to it with its number instead.

Reason: Two copies of a rule drift apart.
