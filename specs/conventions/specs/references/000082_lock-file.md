---
id: "000082"
title: spezi.lock holds the commit and the hash of each copy
kind: convention
status: draft
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/lock.py
  - src/spezi/check.py
  - src/spezi/kit.py
scope:
  - src/spezi/lock.py
  - spezi.toml
---

# spezi.lock holds the commit and the hash of each copy

`ref` in `spezi.toml` must name a tag, a branch or a commit of the repository. The file
`spezi.lock` in the root of the repository must hold one table for each repository of
`spezi.toml` and for each copy of a transitive upstream (000092), in TOML:

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
| `commit` | The commit of the copy below `specs/.upstream/` (000048). |
| `include` | The `include` of `spezi.toml`, or an empty list. For a transitive upstream, the union of 000092. |
| `via` | Only for a transitive upstream: the direct upstreams that name it in `transitive`, sorted. A transitive upstream has no `ref`. |
| `hash` | The SHA-256 hash of the copy. For each file of the copy, in the order of the sorted paths, the hash takes the path below the copy, a null byte, the length of the content, a null byte and the content. It is written as `sha256-` and the hash in Base64. |

Only `spezi install`, `spezi update`, `spezi add` and `spezi init` must write `spezi.lock`
(000083). A person or an agent must not change it. `spezi check` must show an error when
`spezi.lock` does not name each repository of `spezi.toml` and each copy of 000092, and no
other, when `ref` or `include` of the entry of a direct upstream is not the same as in
`spezi.toml`, when `commit`, `include` or `via` of the entry of a transitive upstream does not
agree with 000092, or when the hash of a copy is not the hash of its entry.

Reason: `spezi.toml` tells which version a project wants, and `spezi.lock` tells which commit it
has. `spezi install` can then load a copy without a network when the copy agrees with
`spezi.lock`, and the check finds a copy that a person changed.

Test: `spezi check` fails when a file of a copy changes.
