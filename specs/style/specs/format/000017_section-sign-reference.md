---
id: "000017"
title: Code refers to a rule with the § sign
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-23
implementation:
  - scripts/check_specs.py
  - specs/config.toml
scope:
  - specs/
---

# Code refers to a rule with the § sign

A docstring or a code comment must refer to a rule with `§` and the full rule ID, without a
space, for example `§F/meetings/voting/000024`. A spec, a commit message or a pull request text
must refer to a rule by its number, without `§`, for example `000024`.

`code_dirs` in `specs/config.toml` names the folders that hold the code.

Reason: One search for `§` finds every place in the code that implements a rule.

Test: `scripts/check_specs.py`: every `§` reference in `code_dirs` names a spec that exists,
and no spec has a `§` before a rule number.
