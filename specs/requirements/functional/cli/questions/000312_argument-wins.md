---
id: "000312"
title: A value of the command line replaces its question
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/ask.py
  - src/spezi/kit.py
  - src/spezi/review.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# A value of the command line replaces its question

A value that the command line gives must replace its question (spec 000085).

Reason: A person who gives a value does not get the same question.

Test: `tests/test_questions.py`.
