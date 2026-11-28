---
id: "000318"
title: The questions of spezi update
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_questions.py:test_update_keeps_a_changed_template
implementation:
  - src/spezi/ask.py
  - src/spezi/kit.py
  - src/spezi/review.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# The questions of spezi update

`spezi update` must ask these questions:

| Question | Proposal |
| --- | --- |
| `<ref>`, only when it is not given and the repository has a tag with a higher version than its `ref`: the choices of `spezi add` | The `ref` of `spezi.toml` |
| The transitive upstreams that the new `spezi.lock` of the repository names and `transitive` does not hold, when `-r` is not given: a checklist | None. With `-r`, all without a question. |
| For a repository with `include`: the folders of the new version that the old version does not have and `include` does not hold | No folder. A chosen folder goes to `include`. |
| A project rule in force names a rule of the repository in `replaces` or in its text. The new version replaces or removes that rule. Update anyway? | No, with a risk. The question lists each such reference. |
| For the kit: a template or a skill is not the same as in the kit at the commit of `spezi.lock`. It is also not the same as in the new kit. Overwrite, keep or cancel? | A risk. The question shows the diff from the file of the project to the file of the new kit. `keep` keeps the file of the project. |

Reason: A change that can break the project needs the answer of a person.

Test: `tests/test_questions.py`.
