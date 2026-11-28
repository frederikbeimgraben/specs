---
id: "000341"
title: A word and a sentence have fixed limits
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_ste.py:test_ste_counts_a_sentence_over_two_lines_once
  - tests/test_ste.py:test_ste_keeps_an_abbreviation_in_the_sentence
implementation:
  - src/spezi/ste.py
  - src/spezi/check.py
  - src/spezi/data/ste/
scope:
  - src/spezi/
---

# A word and a sentence have fixed limits

For the check of ASD-STE100 (spec 000093), a word must be a part of the text between spaces with
a letter or a digit. A sentence must end after a word that ends in `.`, `!` or `?`, also before a
closing quote or bracket. An abbreviation of the list does not end a sentence. `e.g.` and other
abbreviations with more than one dot end a sentence only before a capital letter.

Reason: Each run counts the same words and sentences.

Test: `tests/test_ste.py`.
