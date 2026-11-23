# specs

A starter kit for specs: the binding rules of a software project, one rule in one Markdown file.

## What it does

- It gives each rule a fixed ID, for example `F/meetings/voting/000024`. Code refers to a rule
  with `§F/meetings/voting/000024`.
- It records the approval of each rule: `draft`, `approved`, `replaced` or `removed`.
- It makes each change start as a spec. Code starts after the owner approves the spec.
- It checks every spec in CI with one Python script, and it writes the index.

## Spec kinds

| Kind | ID | Folder | Holds |
| --- | --- | --- | --- |
| functional | `F` | `specs/requirements/functional/` | What the product must do. |
| non-functional | `NF` | `specs/requirements/non-functional/` | How well the product must do it. |
| style | `S` | `specs/style/` | How code, tests and texts must look. |
| protocol | `P` | `specs/protocols/` | One data format, with a JSON Schema and an example. |
| structure | `U` | `specs/structures/` | One UML diagram in Mermaid, with an element table. |

## Contents

| Path | Content |
| --- | --- |
| `specs/style/specs/` | The base rules for specs. They are specs too. Read them first. |
| `specs/TEMPLATE*.md` | The templates for a rule, a protocol spec and a structure spec. |
| `specs/structures/` | Two example structure specs. |
| `specs/config.toml` | The settings of the check. |
| `scripts/check_specs.py` | The check. Python 3.11 or later. |
| `.claude/skills/` | Skills for agents: `spec-write`, `spec-structure`, `spec-approve`, `spec-check`, `spec-adopt`. |
| `.github/workflows/specs.yml` | The CI job. |
| `install.sh` | Copies the kit into a project. |

## Add the kit to a project

```sh
git clone --depth 1 https://github.com/frederikbeimgraben/specs /tmp/spec-kit
/tmp/spec-kit/install.sh <project-dir> <owner-login>
```

The installer does not overwrite a file. For a project that has its own specs, follow the skill
[spec-adopt](.claude/skills/spec-adopt/SKILL.md).

## Check

```sh
pip install jsonschema                  # only for JSON protocol specs
python3 scripts/check_specs.py --write  # check, and write the index in specs/README.md
```

All text in this kit follows ASD-STE100 Simplified Technical English (000025).
