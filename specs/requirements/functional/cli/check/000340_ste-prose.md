---
id: "000340"
title: The check of ASD-STE100 reads only the prose
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_ste.py:test_ste_reads_only_the_prose
  - tests/test_ste.py:test_ste_reads_each_list_item_and_cell_alone
implementation:
  - src/spezi/ste.py
  - src/spezi/check.py
  - src/spezi/data/ste/
scope:
  - src/spezi/
---

# The check of ASD-STE100 reads only the prose

The check of ASD-STE100 (spec 000093) must read only the prose of the body: paragraphs, list
items and table cells. It must not read the front matter, headings, code blocks, inline code and
link targets. Each list item and each table cell is a separate text.

Reason: Code and names do not follow the rules of a language.

Test: `tests/test_ste.py`.
