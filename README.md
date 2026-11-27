# specs

A starter kit for specs: the binding rules of a software project, one rule in one Markdown file.
The repository is a Nix flake. Its command `specs` checks and manages the specs of a project.

## What it does

- It gives each rule a fixed number, for example `000024`. Code refers to a rule with `§000024`,
  and to a rule of a different repository with `§github.com/<owner>/<repo>:000024`.
- It records the approval of each rule: `draft`, `approved`, `replaced` or `removed`.
- It makes each change start as a spec. Code starts after the owner approves the spec.
- It checks every spec in CI, and it writes the index.
- It gives agents an MCP server to read, find and create specs.

## Spec kinds

| Kind | ID | Folder | Holds |
| --- | --- | --- | --- |
| functional | `F` | `specs/requirements/functional/` | What the product must do. |
| non-functional | `NF` | `specs/requirements/non-functional/` | How well the product must do it. |
| protocol | `P` | `specs/protocols/` | One data format, with a JSON Schema and an example. |
| structure | `U` | `specs/structures/` | One UML diagram in Mermaid, with an element table. |
| style | `S` | `specs/style/` | How code, tests and product texts must look. |
| convention | `C` | `specs/conventions/` | How specs must look. |
| workflow | `W` | `specs/workflow/` | How people and agents must work. |
| agent | `A` | `specs/agents/` | What only an agent must do or must not do. |
| decision | `D` | `specs/decisions/` | One design decision with its alternatives. |

000004 tells which kind a rule gets.

## Layout of a project

| Path | Content |
| --- | --- |
| `specs/` | Only the rules of the project, and `README.md`, a copy of the index (000051). |
| `.specs/upstream/<host>/<group>/.../<repo>/` | The rules of a different repository, for example of this kit (000048). |
| `.specs/templates/` | The templates for a new spec (000008). |
| `.specs/index.md` | The index of all rules that apply (000007). |
| `specs.toml` | The settings. |
| `.claude/skills/spec-*` | Skills for agents. |
| `.mcp.json` | The MCP server `specs`. |
| `.github/workflows/specs.yml` or `.gitlab/ci/specs.yml`, included from `.gitlab-ci.yml` | The CI job. |

## Commands

```sh
nix run github:frederikbeimgraben/specs/<ref> -- <command>
```

| Command | Effect |
| --- | --- |
| `check [--write]` | Checks the specs and the `§` references. `--write` also writes the index. |
| `init [<dir>] [--forge github\|gitlab]` | Adds the kit to a project. |
| `update [<ref>]` | Updates the kit: the copy of its rules, the templates, the skills, the CI file and the MCP server entry. |
| `update <repo> <ref>` | Replaces the copy of the rules of a different repository. |
| `add <repo> <ref>` | Adds the copy of the rules of a different repository. |
| `new <kind> <area>/<topic> <name> "<title>" [--owner <login>]` | Makes a new spec from its template, with the next number. |
| `resolve <id>` | Prints the long form of an ID, for example `C/specs/format/000012` for `000012`. |
| `show <id>` | Prints the full text of a spec. |
| `list` | Lists every rule. |
| `search <text>` | Lists the rules that hold a text. |
| `mcp` | Runs the MCP server on stdin and stdout. It has the tools `check`, `resolve`, `show`, `list`, `search` and `new`. |

A project runs the command at the `ref` of the kit in `specs.toml`. `init` and `update` write
this `ref` into the CI file and into `.mcp.json`.

## Add the kit to a project

```sh
cd <project-dir>
nix run github:frederikbeimgraben/specs -- init
```

A project numbers its own rules from `000001`. For a project that has its own specs, follow the
skill [spec-adopt](.claude/skills/spec-adopt/SKILL.md).

## Contents of this repository

| Path | Content |
| --- | --- |
| `specs/conventions/specs/` | The conventions for specs. Read them first. |
| `specs/workflow/specs/` | The rules for the change process. |
| `specs/agents/` | The rules for agents. |
| `specs/style/` | The code style, by language. |
| `specs/structures/` | Two example structure specs. |
| `src/specs_kit/` | The command `specs`. |
| `flake.nix` | The Nix flake with the package, the app and a dev shell. |

All text in this kit follows ASD-STE100 Simplified Technical English (000025).
