---
id: "000316"
title: The questions of spezi init
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_questions.py:test_init_writes_the_answers
implementation:
  - src/spezi/ask.py
  - src/spezi/kit.py
  - src/spezi/review.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# The questions of spezi init

`spezi init` must ask these questions:

| Question | Proposal |
| --- | --- |
| The forge, when `--forge` is not given | The forge of `git remote origin` (spec 000066) |
| `base_ref` | The default branch of `origin` that git knows, else `origin/main` |
| `code_dirs`, a checklist of the top folders that git tracks, without hidden folders and `specs/` | The folders with a file of the default `code_suffixes` |
| `code_suffixes`, a checklist of the default types and the types in the chosen `code_dirs` | The types that the chosen `code_dirs` have. Without `code_dirs`, no question and the default types. |
| `repo`, the full name of the project | The name from the URL of `git remote origin`, else empty. Empty gives no `repo`. |
| The transitive upstreams of the kit to copy (spec 000092), when `-r` is not given: a checklist of the repositories in the `spezi.lock` of the kit without `repo` | None. With `-r`, all without a question. |
| The login of the user, only when `git config <forge>.user` has no value | Empty. A login goes to `git config --local <forge>.user`. |
| `[features]`, a checklist of the switches (spec 000084) | Each switch on. `claude` without `agents` asks again. |
| For an `.envrc` without `use flake` and a `CLAUDE.md` without `@AGENTS.md`: add the line? | No |

Reason: Each setting of a new project gets a proposal that fits most projects.

Test: `tests/test_questions.py`.
