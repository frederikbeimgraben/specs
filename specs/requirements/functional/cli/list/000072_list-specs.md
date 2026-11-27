---
id: "000072"
title: specs list prints every rule
kind: functional
status: draft
owner: frederikbeimgraben
updated: 2026-11-27
tests:
  - tests/test_queries.py:test_list_prints_one_line_for_each_rule
implementation:
  - src/specs_kit/queries.py
scope:
  - src/specs_kit/
---

# specs list prints every rule

`specs list` must print one line for each rule of the project, then one line for each rule of
the copies. A line must hold the kind letter, the short form (000047), the status and the title,
in this order and separated by tabs. For example:

```text
S	000060	approved	Python code needs Python 3.13 or later
```

Reason: An agent sees all rules in one call. The short form is the form that code and specs
use, and the kind letter tells the kind without the long path.

Test: `tests/test_queries.py`.
