---
name: spec-adopt
description: Add the spec format of frederikbeimgraben/specs to a new or an existing project, or update a project to a newer version of the kit. Use when a project has no specs/ folder yet, or has its own spec format.
---

# Add the spec format to a project

## New project, or a project without `specs/`

1. Get the kit and run the installer from the project root:

   ```sh
   git clone --depth 1 https://github.com/frederikbeimgraben/specs /tmp/spec-kit
   /tmp/spec-kit/install.sh . <owner-login>
   ```

   The installer copies `specs/`, `scripts/check_specs.py`, the skills and the CI workflow. It
   does not overwrite a file that exists. It sets `owner` to `<owner-login>`.

2. Edit `specs/config.toml`: set `base_ref` to the base branch and `code_dirs` to the folders
   with code.
3. Delete the two example specs in `specs/structures/specs/` if the project does not want them.
   Then run `python3 scripts/check_specs.py --write`.
4. Add the text below to `CLAUDE.md` or `AGENTS.md`.
5. Commit, open a pull request, and ask the owner to approve the rules of `specs/style/specs/`
   (skill `spec-approve`).
6. New rules take the next free number after the kit rules.

## Project with its own `specs/`

1. Run the installer. It copies only the files that do not exist and lists the files that it
   skipped.
2. Compare each skipped file with the kit. Merge by hand.
3. For each kit rule that the project does not have, write a new spec with the next free number
   of the project (skill `spec-write`). Do not take the kit number: a number is the identity of
   a rule (000013).
4. Change the rule numbers in the error texts of `scripts/check_specs.py` to the numbers of the
   project.
5. To add only the structure kind: copy `TEMPLATE-structure.md`, the rules 000033 to 000039 with
   new numbers, the `structures` key and the structure checks of `check_specs.py`.

## Text for CLAUDE.md

```markdown
## Specs

`specs/` holds the binding rules, one rule per file. A spec wins over a skill or a comment.
A change request starts as a spec, and code starts after the owner approves it.
Skills: `spec-write`, `spec-structure`, `spec-approve`, `spec-check`.
Check: `python3 scripts/check_specs.py --write`.
```
