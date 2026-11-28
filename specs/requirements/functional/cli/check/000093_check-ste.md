---
id: "000093"
title: spezi check checks the rules of ASD-STE100
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_ste.py:test_ste_finds_a_long_sentence
  - tests/test_ste.py:test_ste_warns_on_passive_voice
  - tests/test_ste.py:test_ste_warns_on_two_verbs_of_one_group
  - tests/test_ste.py:test_ste_warns_on_two_instructions
  - tests/test_ste.py:test_check_gives_the_warnings_as_json
  - tests/test_ste.py:test_lsp_shows_a_warning_with_the_severity_warning
implementation:
  - src/spezi/ste.py
  - src/spezi/check.py
  - src/spezi/data/ste/
scope:
  - src/spezi/
---

# spezi check checks the rules of ASD-STE100

`spezi check` must check the text of each rule of the project against the rules of ASD-STE100
(spec 000025). Each check gives a warning:

| Check | Condition |
| --- | --- |
| Sentence length | A sentence has more than 25 words. |
| Passive voice | `is`, `are`, `was`, `were`, `been` or `being` comes before a word that ends in `-ed` or a participle of the list. |
| Synonyms | One rule uses two verbs of one group of the list. The warning is at the first place of the second verb. |
| Instructions | One sentence holds two or more of `must`, `do not`, `never` and `shall`. `must not` counts as one. |

Reason: A program finds only possible problems of ASD-STE100. A person reads a warning and
decides.

Test: `tests/test_ste.py`.
