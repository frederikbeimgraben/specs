---
id: "000011"
title: One file holds one rule
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - src/specs_kit/check.py
scope:
  - specs/
---

# One file holds one rule

One spec file must hold exactly one rule. After the front matter come one `#` title, the rule
text and the labels (000015). A spec must not use other headings. A protocol spec has the fixed
`##` sections of 000027. A structure spec has the fixed `##` sections of 000033. A decision
spec has the fixed `##` sections of 000042.

Reason: The rule ID then points to exactly one file and one rule.

Test: `specs check`: the body has the title and only the allowed sections.
