---
id: "000085"
title: init, add and update ask questions on a terminal
kind: functional
status: draft
owner: frederikbeimgraben
updated: 2026-11-27
tests:
  - tests/test_questions.py:test_init_takes_the_proposals_without_a_terminal
  - tests/test_questions.py:test_init_writes_the_answers
  - tests/test_questions.py:test_init_cancel_changes_no_file
  - tests/test_questions.py:test_add_asks_for_the_folders
  - tests/test_questions.py:test_update_keeps_a_changed_template
  - tests/test_questions.py:test_update_stops_for_a_changed_template_without_a_terminal
  - tests/test_questions.py:test_update_stops_for_a_removed_rule_without_a_terminal
implementation:
  - src/specs_kit/ask.py
  - src/specs_kit/kit.py
  - src/specs_kit/review.py
  - src/specs_kit/cli.py
scope:
  - src/specs_kit/
---

# init, add and update ask questions on a terminal

When stdin and stdout are a terminal, `specs init`, `specs add` and `specs update` must ask
the questions of the tables below. Each question must show its proposal. A value that the
command line gives replaces its question. With `-y` (also `--yes` or `--non-interactive`), with
`--json`, or without a terminal, each question must take its proposal. A question that has a
risk must then stop the command with an error. Ctrl+C must stop the command with an error.

`specs init`:

| Question | Proposal |
| --- | --- |
| The forge, when `--forge` is not given | The forge of `git remote origin` (000066) |
| `base_ref` | The default branch of `origin` that git knows, else `origin/main` |
| `code_dirs`, a checklist of the top folders that git tracks, without hidden folders and `specs/` | The folders with a file of the default `code_suffixes` |
| `code_suffixes`, a checklist of the default types and the types in the chosen `code_dirs` | The types that the chosen `code_dirs` have. Without `code_dirs`, no question and the default types. |
| The login of the user, only when `git config <forge>.user` has no value | Empty. A login goes to `git config --local <forge>.user`. |
| `[features]`, a checklist of the switches of 000084 | Each switch on. `claude` without `agents` asks again. |
| For an `.envrc` without `use flake` and a `CLAUDE.md` without `@AGENTS.md`: add the line? | No |

`specs add`:

| Question | Proposal |
| --- | --- |
| `<repo>`, when it is not given | None. The command must check the name with `git ls-remote` and ask again for a bad name. Without a terminal, `<repo>` is necessary. |
| `<ref>`, when it is not given: one of the 10 tags with the highest version, the default branch, or a typed ref | The tag with the highest version (000068) |
| The folders to copy, when `--include` is not given: a checklist of the kind folders and their direct folders | All folders. All folders give no `include`. |

`specs update`:

| Question | Proposal |
| --- | --- |
| `<ref>`, only when it is not given and the repository has a tag with a higher version than its `ref`: the choices of `specs add` | The `ref` of `specs.toml` |
| For a repository with `include`: the folders of the new version that the old version does not have and `include` does not hold | No folder. A chosen folder goes to `include`. |
| A project rule in force names a rule of the repository in `replaces` or in its text, and the new version replaces or removes that rule: update anyway? | No, with a risk. The question lists each such reference. |
| For the kit: a template or a skill is not the same as in the kit at the commit of `specs.lock` and not the same as in the new kit: overwrite, keep or cancel? | A risk. The question shows the diff from the file of the project to the file of the new kit. `keep` keeps the file of the project. |

Before the copy of each repository, `specs init`, `specs add` and `specs update` must show a
summary and ask `Run?`, with the proposal yes. The summary of `specs init` must show the
answers. The summary of `specs add` and `specs update` must show the old and the new `ref`, the
new commit, and each new, changed and removed rule as `A`, `M` or `D` with its number and its
title. When the user answers no, or cancels, the command must stop with an error before it
changes the copy of this repository. A repository that `specs update` updated before stays
updated. `specs init` must not change a file before the answer to `Run?`.

Reason: A person sees and chooses each setting and each version before a command changes the
project, and a script or an agent gets the same result as before without questions. A change
that can break the project never happens without a person.

Test: `tests/test_questions.py`.
