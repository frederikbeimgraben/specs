---
id: "000210"
title: spezi check checks each reference to a rule
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_check.py:test_check_finds_a_reference_to_no_rule
  - tests/test_check.py:test_check_finds_a_reference_to_a_removed_rule
implementation:
  - src/spezi/agents.py
  - src/spezi/check.py
  - src/spezi/index.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# spezi check checks each reference to a rule

`spezi check` must check each reference to a rule in the files of `code_dirs` and in each
Markdown file that git tracks (spec 000017).

Reason: A reference to a rule that is not in force misleads the reader.

Test: `tests/test_check.py`.
