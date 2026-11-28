---
id: "000093"
title: spezi check checks the rules of ASD-STE100
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_ste.py:test_ste_finds_a_long_sentence
  - tests/test_ste.py:test_ste_counts_a_sentence_over_two_lines_once
  - tests/test_ste.py:test_ste_reads_only_the_prose
  - tests/test_ste.py:test_ste_reads_each_list_item_and_cell_alone
  - tests/test_ste.py:test_ste_keeps_an_abbreviation_in_the_sentence
  - tests/test_ste.py:test_ste_warns_on_passive_voice
  - tests/test_ste.py:test_ste_warns_on_two_verbs_of_one_group
  - tests/test_ste.py:test_ste_warns_on_two_instructions
  - tests/test_ste.py:test_check_shows_the_findings
  - tests/test_ste.py:test_check_passes_with_only_warnings
  - tests/test_ste.py:test_check_without_ste
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

`spezi check` must check the text of each rule of the project against the rules of
ASD-STE100 (spec 000025). It must not do this check on the rules of the copies (spec 000065).
With `ste = false` in `spezi.toml` (spec 000078), it must not do this check.

The check must read only the prose of the body: paragraphs, list items and table cells. It must
not read the front matter, headings, code blocks, inline code and link targets. Each list item
and each table cell is a separate text.

Each check must give a warning:

| Check | Condition |
| --- | --- |
| Sentence length | A sentence has more than 25 words. |
| Passive voice | `is`, `are`, `was`, `were`, `been` or `being` comes before a word that ends in `-ed` or a participle of the list. |
| Synonyms | One rule uses two verbs of one group of the list. The warning is at the first place of the second verb. |
| Instructions | One sentence holds two or more of `must`, `do not`, `never` and `shall`. `must not` counts as one. |

A word is a part of the text between spaces with a letter or a digit. A sentence ends after a
word that ends in `.`, `!` or `?`, also before a closing quote or bracket. An abbreviation of the
list does not end a sentence. `e.g.` and other abbreviations with more than one dot end a
sentence only before a capital letter.

The lists of participles, of verb groups and of abbreviations must be in `src/spezi/data/ste/`.
They are a copy of the lists of `github.com/danyuchn/asd-ste100-skill`. The folder must hold the
MIT license of this repository with its source in the file `NOTICE`.

The line of a warning is the line where the sentence starts. A warning line must
be `<path>:<line>: warning: <text>`. The warning lines must come after the error lines. A
warning must not change the exit code (spec 000065).

Reason: A project with old text must pass the check also after an update of the kit. A program
finds only possible problems of ASD-STE100. A person reads a warning and decides.

Test: `tests/test_ste.py`.
