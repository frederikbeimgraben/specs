---
id: "000082"
title: spezi.lock holds the commit and the hash of each copy
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_transitive.py:test_the_lock_keeps_via_and_no_ref
implementation:
  - src/spezi/lock.py
  - src/spezi/check.py
  - src/spezi/kit.py
scope:
  - src/spezi/lock.py
  - spezi.toml
---

# spezi.lock holds the commit and the hash of each copy

The file `spezi.lock` in the root of the repository must be in TOML. It must hold one table for
each repository of `spezi.toml` and for each copy of a transitive upstream (spec 000092):

```toml
[upstream."github.com/frederikbeimgraben/spezi"]
ref = "v1.2"
commit = "<the commit that ref named>"
include = []
hash = "sha256-<base64>"
```

| Key | Content |
| --- | --- |
| `ref` | The `ref` of `spezi.toml` that gave the commit. |
| `commit` | The commit of the copy below `specs/.upstream/` (spec 000048). |
| `include` | The `include` of `spezi.toml`, or an empty list. For a transitive upstream, the union (spec 000092). |
| `via` | Only for a transitive upstream: the direct upstreams that name it in `transitive`, sorted. A transitive upstream has no `ref`. |
| `hash` | The SHA-256 hash of the copy. The hash takes each file of the copy in the order of the sorted paths. For each file, it takes the path below the copy, a null byte, the length of the content, a null byte and the content. The value is `sha256-` and the hash in Base64. |

Reason: `spezi.toml` tells which version a project wants, and `spezi.lock` tells which commit it
has. `spezi install` can then load a copy without a network when the copy agrees with
`spezi.lock`.

Test: `tests/test_transitive.py`.
