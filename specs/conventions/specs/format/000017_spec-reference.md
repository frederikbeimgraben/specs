---
id: "000017"
title: Code refers to a rule with (spec <number>)
kind: convention
status: draft
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
  - spezi.toml
scope:
  - specs/
---

# Code refers to a rule with (spec <number>)

A text must refer to a rule with `(spec <ref>)`. `<ref>` is the short form of the rule
(spec 000047). Examples: `(spec 000024)`, `(spec github.com/frederikbeimgraben/spezi:000012)`.

This rule applies to these texts:

1. A docstring and a code comment in the folders of `code_dirs` in `spezi.toml`.
2. A spec and each other Markdown file that git tracks.
3. A commit message and the text of a pull request.

One pair of parentheses can hold a list of rules. A `, ` must separate two items. An item is a
local or a foreign short form, for example `(spec 000088, 000089)` or
`(spec 000088, github.com/frederikbeimgraben/spezi:000012)`. A range of numbers is not
permitted.

In a Markdown file, a rule number must not stand outside `(spec ...)`. Three parts are
permitted exceptions: the front matter, the tables that `spezi` writes, and text in backticks
or in a code block.

Reason: One search for `(spec ` finds every text that refers to a rule. Code and text use one
form.

Test: `spezi check`: every `(spec ...)` holds only short forms of rules that exist. No text
of 1. or 2. has `§` before a rule number. No Markdown file has a rule number outside
`(spec ...)`, outside the three exceptions.
