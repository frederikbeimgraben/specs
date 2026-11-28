---
name: spezi-adopt
description: Add the spec format of frederikbeimgraben/spezi to a new or an existing project, or update a project to a newer version of the kit. Use when a project has no specs/ folder yet, or has its own spec format.
---

# Add the spec format to a project

`spezi` is the command of the kit. Run it with Nix as
`nix run github:frederikbeimgraben/spezi/<commit> -- <command>`, with the commit of the kit in
`spezi.lock`.

## New project, or a project without `specs/`

1. Run `init` in the project root:

   ```sh
   nix run github:frederikbeimgraben/spezi -- init
   ```

   `init` writes `spezi.toml` and `spezi.lock`, makes `specs/`, and puts the rules of the kit in
   `specs/.upstream/github.com/frederikbeimgraben/spezi/` as an unchanged copy (spec 000048). It
   copies the templates to `specs/.templates/` and the skills to `.claude/skills/`. It writes the
   CI file (`.github/workflows/spezi.yml` or `.gitlab/ci/spezi.yml`, included from `.gitlab-ci.yml`) and the MCP server `spezi` in
   `.mcp.json`. It finds the forge in `git remote origin`. Give `--forge github` or
   `--forge gitlab` if it cannot.

2. Edit `spezi.toml`: set `base_ref` to the base branch and `code_dirs` to the folders with code.
3. Run `spezi install`.
4. Add the text below to `CLAUDE.md` or `AGENTS.md`.
5. Commit and open a pull request.
6. The project numbers its own rules from `000001`. A reference to a kit rule has the form
   `github.com/frederikbeimgraben/spezi:<number>` (spec 000047).

## Project with its own `specs/`

1. Move the files in `specs/` that are not rules out of `specs/` (spec 000051). Move an old
   `specs/config.toml` to `spezi.toml`.
2. Run `init`. It stops if `spezi.toml` exists. Then merge the settings by hand.
3. Compare the rules of the project with the kit rules in `specs/.upstream/`. If a project rule
   contradicts a kit rule, ask the owner which one applies. Replace the kit rule with
   `replaces`, or change the project rule (spec 000050).
4. Move the project specs to the kind folders (spec 000004). A moved rule keeps its number (spec 000014).

## Update the kit

1. Run `spezi update kit`. It resolves the `ref` of the kit in `spezi.toml` again. To change the
   version, run `spezi update kit <ref>`. It replaces the copy, the templates, the skills, the CI
   file and the MCP server entry, and writes the new commit to `spezi.lock` (spec 000048, 000082).
   `spezi update` without arguments does this for each repository of `spezi.toml`.
2. Read the diff of the copy. Replace a new rule that must not apply with `replaces` (spec 000049),
   and fix each error. Open a pull request.

The rules of a different repository: `spezi add <repo> [<ref>]` adds a copy, and
`spezi update <repo> [<ref>]` replaces it. After a clone, or when a file of the kit is missing,
run `spezi install`. It changes no version (spec 000083). `<repo>` is the full path, with each GitLab subgroup.
To take only some rules, add `--include <folder>` once for each folder below `specs/`, for
example `--include style/python/`.

## Text for CLAUDE.md

```markdown
## Specs

`specs/` holds the binding rules of the project, one rule per file. A spec wins over a skill or a comment.
`specs/.upstream/` holds the rules of different repositories. They apply, except a rule that a
project spec names in `replaces`. `specs/README.md` lists all rules that apply.
Rules for agents are in the kind folder `agents/`. Read them before each task.
A change request starts as a spec, and code starts after the owner approves it.
Skills: `spezi-write`, `spezi-structure`, `spezi-approve`, `spezi-check`.
Command: `nix run github:frederikbeimgraben/spezi/<commit> -- <command>`, with the commit of the
kit in `spezi.lock`, or the MCP server `spezi`. Check: `spezi check`. After a change of a rule:
`spezi install`.
```
