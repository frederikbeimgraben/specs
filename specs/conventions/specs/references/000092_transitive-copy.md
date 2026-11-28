---
id: "000092"
title: A copy brings the upstreams of its repository
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_transitive.py:test_add_with_recursive_copies_the_transitive_upstream
implementation:
  - src/spezi/transitive.py
  - src/spezi/kit.py
  - src/spezi/check.py
scope:
  - specs/
  - spezi.toml
---

# A copy brings the upstreams of its repository

A direct upstream is a repository with a table `[upstream."<repo>"]` in `spezi.toml`. Its
`spezi.lock` names its own upstreams, direct and transitive. These are the transitive upstreams
of the project. The list `transitive` in the table of the direct upstream must name each
transitive upstream that the project copies:

```toml
repo = "github.com/frederikbeimgraben/spezi"

[upstream."github.com/frederikbeimgraben/spezi-python"]
ref = "v1.0"
transitive = ["github.com/example/other"]
```

Reason: A rule of an upstream can refer to a rule of its own upstream. The copy of that
upstream makes the reference readable without a network.

Test: `tests/test_transitive.py`.
