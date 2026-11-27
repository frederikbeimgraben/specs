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
| style | `S` | `specs/style/` | How code and tests must look. |
| convention | `C` | `specs/conventions/` | How specs must look. |
| workflow | `W` | `specs/workflow/` | How people and agents must work. |
| agent | `A` | `specs/agents/` | What only an agent must do or must not do. |
| decision | `D` | `specs/decisions/` | One design decision with its alternatives. |

000004 tells which kind a rule gets.

## Layout of a project

| Path | Content |
| --- | --- |
| `specs/` | The rules of the project in the kind folders, and `README.md`, the index (000051). |
| `specs/.upstream/<host>/<group>/.../<repo>/` | The rules of a different repository, for example of this kit (000048). |
| `specs/.templates/` | The templates for a new spec (000008). |
| `specs.toml` | The settings, with the switches of the optional parts in `[features]` (000078, 000084). |
| `specs.lock` | The commit and the hash of each copy below `specs/.upstream/` (000082). |
| `.claude/skills/spec-*` | Skills for agents. |
| `.mcp.json` | The MCP server `specs`. |
| `.github/workflows/specs.yml`, `.gitlab/ci/specs.yml` (included from `.gitlab-ci.yml`) or `.forgejo/workflows/specs.yml` | The CI job. |
| `AGENTS.md`, `CLAUDE.md` | The rules for agents, written by `specs install`, and the import `@AGENTS.md` (000079). |
| `flake.nix`, `flake.lock`, `.envrc` | The devShell with the command `specs` at the commit of the kit (000066). |

## Commands

```sh
nix run github:frederikbeimgraben/specs/<commit> -- <command>
```

| Command | Effect |
| --- | --- |
| `check` | Checks the specs and the `§` references. It changes no file. |
| `install` | Loads each copy that does not agree with `specs.lock`, writes each missing file of the kit, the index and `AGENTS.md`, then checks. It changes no version (000083). |
| `init [<dir>] [--forge github\|gitlab\|codeberg]` | Adds the kit to a project, and a devShell with the command when the project has no `flake.nix`. |
| `update [<repo> [<ref>]]` | Resolves the `ref` of each repository, or of one, again and replaces its copy. With `<ref>`, it first sets `ref` in `specs.toml`. `<repo>` can be `kit`. For the kit, it also replaces the templates, the skills, the CI file, the MCP server entry and the input `specs` in `flake.nix`. |
| `add <repo> [<ref>] [--include <folder>]...` | Adds the copy of the rules of a different repository, at `<ref>` or at its tag with the highest version. |
| `new <kind> <area>/<topic> <name> "<title>" --scope <path>... [--owner <login>]` | Makes a new spec from its template, with the next number and the paths of `scope`. |
| `resolve <id>` | Prints the long form of an ID, for example `C/specs/format/000012` for `000012`. |
| `show <id>` | Prints the full text of a spec. |
| `list` | Lists every rule. |
| `search <text>` | Lists the rules that hold a text. |
| `mcp` | Runs the MCP server on stdin and stdout. It has the tools `check`, `install`, `resolve`, `show`, `list`, `search` and `new`. |

A project runs the command at the commit of the kit in `specs.lock`. `init` and `update` write
this commit into the CI file, into `.mcp.json` and into the input `specs` of `flake.nix`.
With direnv, the devShell loads the new command after `specs update`.

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
