---
id: "000099"
title: The unit tests of a rule are in tests
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/
scope:
  - specs/
---

# The unit tests of a rule are in tests

A unit test that checks a rule must be in the front matter key `tests` of the rule
(spec 000009).

Reason: `tests` lets a tool find the tests of a rule and run them.
