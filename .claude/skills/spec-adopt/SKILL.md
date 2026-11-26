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

   The installer copies the templates, `specs/config.toml`, `scripts/check_specs.py`, the skills
   and the CI workflow. It does not overwrite a file that exists. It sets `owner` in the
   templates to `<owner-login>`. The rules of the kit go to
   `specs/upstream/github.com/frederikbeimgraben/specs/` as an unchanged copy (000048), and
   `specs/config.toml` gets their `ref`.

2. Edit `specs/config.toml`: set `base_ref` to the base branch and `code_dirs` to the folders
   with code.
3. Run `python3 scripts/check_specs.py --write`.
4. Add the text below to `CLAUDE.md` or `AGENTS.md`.
5. Commit and open a pull request.
6. The project numbers its own rules from `000001`. A reference to a kit rule has the form
   `github.com/frederikbeimgraben/specs:<ID>` (000047).

## Project with its own `specs/`

1. Run the installer. It copies only the files that do not exist and lists the files that it
   skipped.
2. Compare each skipped file with the kit. Merge by hand.
3. Compare the rules of the project with the kit rules in `specs/upstream/`. If a project rule
   contradicts a kit rule, ask the owner which one applies. Replace the kit rule with `replaces`, or change
   the project rule (000050).
4. Move the project specs to the kind folders of 000004. A moved rule keeps its number (000014).

## Update the kit

1. Set `ref` of `github.com/frederikbeimgraben/specs` in `specs/config.toml` to the new tag or
   commit.
2. Run `python3 scripts/check_specs.py --fetch --write`. It replaces the copy (000048).
3. Copy the new `scripts/check_specs.py` and the skills from the kit.
4. Read the diff of the copy. Replace a new rule that must not apply with `replaces` (000049), and fix each
   error. Open a pull request.

## Text for CLAUDE.md

```markdown
## Specs

`specs/` holds the binding rules, one rule per file. A spec wins over a skill or a comment.
`specs/upstream/` holds the rules of the kit. They apply, except a rule that a project spec
names in `replaces`.
`specs/agents/` holds the rules for agents. Read them before each task.
A change request starts as a spec, and code starts after the owner approves it.
Skills: `spec-write`, `spec-structure`, `spec-approve`, `spec-check`.
Check: `python3 scripts/check_specs.py --write`.
```
