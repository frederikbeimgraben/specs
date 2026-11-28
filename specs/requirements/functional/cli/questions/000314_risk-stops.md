---
id: "000314"
title: A question with a risk stops a command without a terminal
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_questions.py:test_update_stops_for_a_changed_template_without_a_terminal
  - tests/test_questions.py:test_update_stops_for_a_removed_rule_without_a_terminal
implementation:
  - src/spezi/ask.py
  - src/spezi/kit.py
  - src/spezi/review.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# A question with a risk stops a command without a terminal

Without a terminal or with `-y`, a question with a risk (spec 000085) must stop the command with
an error.

Reason: A change that can break the project never happens without a person.

Test: `tests/test_questions.py`.
