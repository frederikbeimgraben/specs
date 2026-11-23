---
id: "000011"
title: One file holds one rule
kind: style
status: draft
owner: frederikbeimgraben
updated: 2026-11-23
implementation:
  - scripts/check_specs.py
scope:
  - specs/
---

# One file holds one rule

One spec file must hold exactly one rule. After the front matter come one `#` title, the rule
text and the labels (000015). A spec must not use other headings. A protocol spec has the fixed
`##` sections of 000027. A structure spec has the fixed `##` sections of 000033.

Reason: The rule ID then points to exactly one file and one rule.

Test: `scripts/check_specs.py`: the body has the title and only the allowed sections.
