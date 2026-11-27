---
id: "000082"
title: specs.lock holds the commit and the hash of each copy
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
implementation:
  - src/specs_kit/lock.py
  - src/specs_kit/check.py
  - src/specs_kit/kit.py
scope:
  - src/specs_kit/lock.py
  - specs.toml
---

# specs.lock holds the commit and the hash of each copy

`ref` in `specs.toml` must name a tag, a branch or a commit of the repository. The file
`specs.lock` in the root of the repository must hold one table for each repository of
`specs.toml`, in TOML:

```toml
[upstream."github.com/frederikbeimgraben/specs"]
ref = "v1.2"
commit = "<the commit that ref named>"
include = []
hash = "sha256-<base64>"
```

| Key | Content |
| --- | --- |
| `ref` | The `ref` of `specs.toml` that gave the commit. |
| `commit` | The commit of the copy below `specs/.upstream/` (000048). |
| `include` | The `include` of `specs.toml`, or an empty list. |
| `hash` | The SHA-256 hash of the copy. For each file of the copy, in the order of the sorted paths, the hash takes the path below the copy, a null byte, the length of the content, a null byte and the content. It is written as `sha256-` and the hash in Base64. |

Only `specs install`, `specs update`, `specs add` and `specs init` must write `specs.lock`
(000083). A person or an agent must not change it. `specs check` must show an error when
`specs.toml` and `specs.lock` do not name the same repositories, when `ref` or `include` of an
entry is not the same as in `specs.toml`, or when the hash of a copy is not the hash of its
entry.

Reason: `specs.toml` tells which version a project wants, and `specs.lock` tells which commit it
has. `specs install` can then load a copy without a network when the copy agrees with
`specs.lock`, and the check finds a copy that a person changed.

Test: `specs check` fails when a file of a copy changes.
