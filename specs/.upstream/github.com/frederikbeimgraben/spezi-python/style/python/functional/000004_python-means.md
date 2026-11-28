---
id: "000004"
title: Python code uses fixed means for the functional style
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# Python code uses fixed means for the functional style

Python code must use these means for the rules of the functional style:

| Rule | Python means |
| --- | --- |
| github.com/frederikbeimgraben/spezi:000054 | No `+=`, no second assignment to a local. |
| github.com/frederikbeimgraben/spezi:000055 | No `.append`, `.add`, `.update`, `.extend`, `x[k] = v` or `del`. |
| github.com/frederikbeimgraben/spezi:000056 | A list, set or dict comprehension, or a generator expression. |
| github.com/frederikbeimgraben/spezi:000057 | `match` with `assert_never` from `typing` in the last case when the type checker cannot see that the match is exhaustive. |
| github.com/frederikbeimgraben/spezi:000058 | `@dataclass(frozen=True, slots=True)`, with fields of the types `tuple`, `frozenset` or `Mapping`. |

Reason: One fixed means for each rule makes the code of two agents look the same.

Test: The ruff rules `C4`, `PERF401`, `PERF402`, `SIM108`, `RET`, `PLW2901` and `FURB`, and
`reportMatchNotExhaustive` of basedpyright. A review checks the rest.
