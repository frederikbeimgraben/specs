---
id: "000313"
title: Without a terminal, each question takes its proposal
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_questions.py:test_init_takes_the_proposals_without_a_terminal
implementation:
  - src/spezi/ask.py
  - src/spezi/kit.py
  - src/spezi/review.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# Without a terminal, each question takes its proposal

With `-y` (also `--yes` or `--non-interactive`), with `--json`, or without a terminal, each
question (spec 000085) must take its proposal.

Reason: A script or an agent gets the same result as before without questions.

Test: `tests/test_questions.py`.
