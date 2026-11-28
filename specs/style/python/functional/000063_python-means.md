---
id: "000063"
title: Python code uses fixed means for the functional style
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
implementation:
  - src/spezi/
scope:
  - src/
---

# Python code uses fixed means for the functional style

Python code must use these means for the rules of the functional style:

| Rule | Python means |
| --- | --- |
| 000054 | No `+=`, no second assignment to a local. |
| 000055 | No `.append`, `.add`, `.update`, `.extend`, `x[k] = v` or `del`. |
| 000056 | A list, set or dict comprehension, or a generator expression. |
| 000057 | `match` with `assert_never` from `typing` in the last case when the type checker cannot see that the match is exhaustive. |
| 000058 | `@dataclass(frozen=True, slots=True)`, with fields of the types `tuple`, `frozenset` or `Mapping`. |

Reason: One fixed means for each rule makes the code of two agents look the same.

Test: The ruff rules `C4`, `PERF401`, `PERF402`, `SIM108`, `RET`, `PLW2901` and `FURB`, and
`reportMatchNotExhaustive` of basedpyright. A review checks the rest.
