# Spezi

A starter kit for specs: the binding rules of a software project, one rule in one Markdown file.
The repository is a Nix flake. Its command `spezi` checks and manages the specs of a project.
The command `specs` is a second name of the same command.

## What it does

- It gives each rule a fixed number, for example `000024`. Code and text refer to a rule with
  `(spec 000024)`, and to a rule of a different repository with
  `(spec github.com/<owner>/<repo>:000024)`.
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

(spec 000004) tells which kind a rule gets.

## Layout of a project

| Path | Content |
| --- | --- |
| `specs/` | The rules of the project in the kind folders, and `README.md`, the index (spec 000051). |
| `specs/.upstream/<host>/<group>/.../<repo>/` | The rules of a different repository, for example of this kit (spec 000048). |
| `specs/.templates/` | The templates for a new spec (spec 000008). |
| `spezi.toml` | The settings, with the switches of the optional parts in `[features]` (spec 000078, 000084). |
| `spezi.lock` | The commit and the hash of each copy below `specs/.upstream/` (spec 000082). |
| `.claude/skills/spezi-*` | Skills for agents. |
| `.mcp.json` | The MCP server `spezi`. |
| `.github/workflows/spezi.yml`, `.gitlab/ci/spezi.yml` (included from `.gitlab-ci.yml`) or `.forgejo/workflows/spezi.yml` | The CI job. |
| `AGENTS.md`, `CLAUDE.md` | The rules for agents, written by `spezi install`, and the import `@AGENTS.md` (spec 000079). |
| `flake.nix`, `flake.lock`, `.envrc` | The devShell with the command `spezi` at the commit of the kit (spec 000066). |

## Commands

```sh
nix run github:frederikbeimgraben/spezi/<commit> -- <command>
```

| Command | Effect |
| --- | --- |
| `check` | Checks the specs and the references to rules. It changes no file. |
| `install` | Loads each copy that does not agree with `spezi.lock`, writes each missing file of the kit, the index and `AGENTS.md`, then checks. It changes no version (spec 000083). |
| `init [<dir>] [--forge github\|gitlab\|codeberg] [-r]` | Asks for the settings, then adds the kit to a project, and a devShell with the command when the project has no `flake.nix`. |
| `update [<repo> [<ref>]] [-r]` | Resolves the `ref` of each repository, or of one, again and replaces its copy. With `<ref>`, it first sets `ref` in `spezi.toml`. `<repo>` can be `kit`. For the kit, it also replaces the templates, the skills, the CI file, the MCP server entry and the input `spezi` in `flake.nix`. |
| `add [<repo> [<ref>]] [--include <folder>]... [-r]` | Adds the copy of the rules of a different repository, at `<ref>` or at its tag with the highest version. |
| `configure [<key> <value>]` | Changes `spezi.toml` in a menu, or sets one key such as `features.mcp false`, then installs (spec 000086). |
| `remove <repo>` | Removes the copy of a different repository, then installs (spec 000087). |
| `new <kind> <area>/<topic> <name> "<title>" --scope <path>... [--owner <login>]` | Makes a new spec from its template, with the next number and the paths of `scope`. |
| `resolve <id>` | Prints the long form of an ID, for example `C/specs/format/000012` for `000012`. |
| `show <id>` | Prints the full text of a spec. |
| `list` | Lists every rule. |
| `search <text>` | Lists the rules that hold a text. |
| `setup-ide zed\|code` | Writes the extension of the language server for Zed or VS Code to `.zed/spezi/` or `.vscode/spezi/` (spec 000089). |
| `lsp` | Runs the language server on stdin and stdout. It shows the errors of the check at their line, and the rule of a reference in a hover (spec 000088). |
| `mcp` | Runs the MCP server on stdin and stdout. It has the tools `check`, `install`, `resolve`, `show`, `list`, `search`, `new`, `configure` and `remove`. |

On a terminal, `init`, `add`, `update` and `configure` ask questions. `-y` takes the proposals
instead, as does a run without a terminal (spec 000085). `init`, `add` and `update` also ask which
upstreams of an upstream to copy, from its `spezi.lock`. `-r` takes each of them without a
question. Without `-r`, a run without a terminal takes none. `repo` in `spezi.toml` names the
project, so that a cycle of upstreams stops (spec 000092).

A project runs the command at the commit of the kit in `spezi.lock`. `init` and `update` write
this commit into the CI file, into `.mcp.json` and into the input `spezi` of `flake.nix`.
With direnv, the devShell loads the new command after `spezi update`.

## Add the kit to a project

```sh
cd <project-dir>
nix run github:frederikbeimgraben/spezi -- init
```

A project numbers its own rules from `000001`. For a project that has its own specs, follow the
skill [spezi-adopt](.claude/skills/spezi-adopt/SKILL.md).

## Contents of this repository

| Path | Content |
| --- | --- |
| `specs/conventions/specs/` | The conventions for specs. Read them first. |
| `specs/workflow/specs/` | The rules for the change process. |
| `specs/agents/` | The rules for agents. |
| `specs/style/` | The code style, by language. |
| `specs/structures/` | Two example structure specs. |
| `src/spezi/` | The command `spezi`. |
| `flake.nix` | The Nix flake with the package, the app and a dev shell. |

All text in this kit follows ASD-STE100 Simplified Technical English (spec 000025).
