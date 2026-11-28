---
id: "000028"
title: The rule selection of ruff holds these rules
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# The rule selection of ruff holds these rules

The rule selection of ruff in `pyproject.toml` must hold these rules:

| Rule | Checks |
| --- | --- |
| `ANN` | Each parameter and each return value of a function has a type. |
| `D` with `convention = "google"` | A docstring has the Google format. A public name has a docstring (spec 000003). |
| `C4`, `PERF401`, `PERF402` | A loop that builds a value is a comprehension (spec 000024). |
| `SIM108` | A branch with two outcomes is a conditional expression (spec github.com/frederikbeimgraben/spezi-functional:000012). |
| `RET` | A function has no `else` after a `return` and no assignment just before its `return` (spec github.com/frederikbeimgraben/spezi-functional:000001). |
| `PLW2901` | A loop does not give its variable a new value (spec 000004). |
| `FURB` | Code uses the current forms of Python. |
| `E722`, `BLE001` | An `except` clause names a concrete class. |
| `S110`, `SIM105` | An `except` clause does not hold only `pass`. To ignore an error, code uses `contextlib.suppress`. |
| `B904` | An `except` clause that raises a new exception uses `raise ... from`. |
| `N` | Names follow the PEP 8 cases. |
| `TID252` with `ban-relative-imports = "all"` | Imports are absolute. |
| `F403` | Code has no star import. |
| `I` | Imports are in the order of ruff. |
| `PT009`, `PT027` | A test does not use the checks of `unittest` (spec 000032). |
| `PGH004` | A `# noqa` comment names the code of the rule (spec 000030). |

Reason: ruff checks these rules, so they need no spec of their own.

Test: A review compares the selection in `pyproject.toml` with this table.
