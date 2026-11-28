---
id: "000317"
title: The questions of spezi add
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_questions.py:test_add_asks_for_the_folders
implementation:
  - src/spezi/ask.py
  - src/spezi/kit.py
  - src/spezi/review.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# The questions of spezi add

`spezi add` must ask these questions:

| Question | Proposal |
| --- | --- |
| `<repo>`, when it is not given | None. The command checks the name with `git ls-remote` and asks again for a bad name. Without a terminal, `<repo>` is necessary. |
| `<ref>`, when it is not given: one of the 10 tags with the highest version, the default branch, or a typed ref | The tag with the highest version (spec 000068) |
| The folders to copy, when `--include` is not given: a checklist of the kind folders and their direct folders | All folders. All folders give no `include`. |
| The transitive upstreams to copy (spec 000092), when `-r` is not given: a checklist of the repositories in the `spezi.lock` of `<repo>` without `repo` and without a repository of `spezi.toml` | None. With `-r`, all without a question. |

Reason: The person chooses the version and the part of the rules to copy.

Test: `tests/test_questions.py`.
