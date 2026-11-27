---
id: "000017"
title: Code refers to a rule with the § sign
kind: convention
status: draft
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - src/specs_kit/check.py
  - specs.toml
scope:
  - specs/
---

# Code refers to a rule with the § sign

A docstring or a code comment must refer to a rule with `§` and the short form of 000047,
without a space, for example `§000024` or `§github.com/frederikbeimgraben/specs:000012`. A
spec, a commit message or a pull request text must refer to a rule by its number, without `§`,
for example `000024`.

`code_dirs` in `specs.toml` names the folders that hold the code.

Reason: One search for `§` finds every place in the code that implements a rule.

Test: `specs check`: every `§` reference in `code_dirs` uses the short form and names a spec
that exists, and no spec has a `§` before a rule number.
