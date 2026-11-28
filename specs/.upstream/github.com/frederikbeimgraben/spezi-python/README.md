# Specs

The binding rules of this project. The kind folders of `specs/` hold the rules
of the project, `specs/.upstream/` the rules of different repositories and
`specs/.templates/` the templates. The command `spezi install` writes this
file. Do not change it by hand (000007).

A new spec starts with
`spezi new <kind> <area>/<topic> <name> "<title>" --scope <path>` (000008).

## Tree

```
specs/
  style/
    python/  docs, functional, lint, typing, version
  .upstream/
    github.com/frederikbeimgraben/spezi/
    github.com/frederikbeimgraben/spezi-functional/
```

## Index

| ID | Title | Status |
| --- | --- | --- |
| [S/python/docs/000003](/specs/style/python/docs/000003_docstrings.md) | Python code is documented in Google-style docstrings | approved |
| [S/python/functional/000004](/specs/style/python/functional/000004_python-means.md) | Python code uses fixed means for the functional style | approved |
| [S/python/lint/000005](/specs/style/python/lint/000005_ruff-clean.md) | ruff reports no warning | approved |
| [S/python/lint/000006](/specs/style/python/lint/000006_ruff-format.md) | ruff format changes nothing | approved |
| [S/python/typing/000002](/specs/style/python/typing/000002_strict-types.md) | Python code is strictly typed | approved |
| [S/python/version/000001](/specs/style/python/version/000001_python-313.md) | Python code needs Python 3.13 or later | approved |

## Upstream

The rules of different repositories that apply to this project (000049).

| ID | Title | Status |
| --- | --- | --- |
| [github.com/frederikbeimgraben/spezi-functional:S/shared/functional/000001](/specs/.upstream/github.com/frederikbeimgraben/spezi-functional/style/shared/functional/000001_body-shape.md) | A function body has one shape | approved |
| [github.com/frederikbeimgraben/spezi-functional:S/shared/functional/000002](/specs/.upstream/github.com/frederikbeimgraben/spezi-functional/style/shared/functional/000002_readability-limit.md) | Readability limits the single expression | approved |
| [github.com/frederikbeimgraben/spezi-functional:S/shared/functional/000003](/specs/.upstream/github.com/frederikbeimgraben/spezi-functional/style/shared/functional/000003_bind-once.md) | A local is bound once | approved |
| [github.com/frederikbeimgraben/spezi-functional:S/shared/functional/000004](/specs/.upstream/github.com/frederikbeimgraben/spezi-functional/style/shared/functional/000004_no-mutation.md) | A value is not mutated | approved |
| [github.com/frederikbeimgraben/spezi-functional:S/shared/functional/000005](/specs/.upstream/github.com/frederikbeimgraben/spezi-functional/style/shared/functional/000005_comprehensions.md) | Comprehensions instead of loops | approved |
| [github.com/frederikbeimgraben/spezi-functional:S/shared/functional/000006](/specs/.upstream/github.com/frederikbeimgraben/spezi-functional/style/shared/functional/000006_exhaustive-match.md) | A branch on one value is an exhaustive match | approved |
| [github.com/frederikbeimgraben/spezi-functional:S/shared/functional/000007](/specs/.upstream/github.com/frederikbeimgraben/spezi-functional/style/shared/functional/000007_frozen-data.md) | Data types are frozen by default | approved |
| [github.com/frederikbeimgraben/spezi-functional:S/shared/functional/000008](/specs/.upstream/github.com/frederikbeimgraben/spezi-functional/style/shared/functional/000008_exceptions.md) | The exceptions of the functional style are named | approved |
| [github.com/frederikbeimgraben/spezi:A/work/approval/000045](/specs/.upstream/github.com/frederikbeimgraben/spezi/agents/work/approval/000045_one-spec-per-question.md) | An agent asks for the approval of one spec in one question | approved |
| [github.com/frederikbeimgraben/spezi:A/work/approval/000046](/specs/.upstream/github.com/frederikbeimgraben/spezi/agents/work/approval/000046_show-the-whole-spec.md) | An agent shows the whole spec for its approval | approved |
| [github.com/frederikbeimgraben/spezi:A/work/questions/000043](/specs/.upstream/github.com/frederikbeimgraben/spezi/agents/work/questions/000043_ask-each-detail.md) | An agent asks the user about each open detail | approved |
| [github.com/frederikbeimgraben/spezi:A/work/questions/000044](/specs/.upstream/github.com/frederikbeimgraben/spezi/agents/work/questions/000044_follow-the-spec.md) | To follow a spec is not an assumption | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/content/000018](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/content/000018_only-the-rule.md) | A spec contains only the rule | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/content/000019](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/content/000019_one-thing.md) | One rule controls one thing | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/content/000020](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/content/000020_examinable.md) | A rule can be examined | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/content/000021](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/content/000021_must-and-must-not.md) | The rule text uses must and must not | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/content/000022](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/content/000022_reason.md) | A rule gives its reason | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/content/000023](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/content/000023_test.md) | A rule names its test | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/content/000024](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/content/000024_current-rule.md) | A spec states the current rule | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/content/000025](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/content/000025_ste.md) | A spec is written in ASD-STE100 | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/content/000026](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/content/000026_product-terms.md) | Product terms stay as the product shows them | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/decisions/000042](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/decisions/000042_whole-decision.md) | A decision spec records one decision with its alternatives | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/format/000008](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/format/000008_copy-the-template.md) | A new spec starts as a copy of the template | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/format/000009](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/format/000009_front-matter.md) | A spec starts with a YAML front matter | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/format/000010](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/format/000010_status.md) | The status shows the approval | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/format/000011](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/format/000011_one-rule-per-file.md) | One file holds one rule | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/format/000012](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/format/000012_rule-id.md) | The rule ID has kind, path and number | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/format/000013](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/format/000013_unique-number.md) | The number is the identity of a rule | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/format/000014](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/format/000014_moved-rule.md) | A moved rule keeps its number | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/format/000015](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/format/000015_labels.md) | Labels in a rule are fixed | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/format/000016](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/format/000016_file-name.md) | The file name is number and name | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/format/000017](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/format/000017_section-sign-reference.md) | Code refers to a rule with the § sign | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/layout/000004](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/layout/000004_tree.md) | The tree sorts by kind, then by area and topic | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/layout/000005](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/layout/000005_folder-names.md) | Folder names are lower case kebab case | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/layout/000006](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/layout/000006_one-place.md) | A rule is written in one place | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/layout/000007](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/layout/000007_index.md) | The index lists every rule | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/layout/000051](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/layout/000051_project-rules-only.md) | specs/ holds the rules of the project and the files of the kit | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/protocols/000027](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/protocols/000027_whole-format.md) | A protocol spec describes one whole format | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/protocols/000028](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/protocols/000028_schema-file.md) | A JSON format has a JSON Schema file beside its spec | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/protocols/000029](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/protocols/000029_checked-example.md) | The example of a JSON format matches its schema | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/protocols/000030](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/protocols/000030_breaking-change.md) | A breaking change of a format is a new protocol spec | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/protocols/000031](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/protocols/000031_code-against-schema.md) | A test checks the output of the code against the schema | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/protocols/000032](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/protocols/000032_protocols-key.md) | A rule names the formats that it uses | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/references/000047](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/references/000047_foreign-reference.md) | A reference to a rule of a different repository names the repository | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/references/000048](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/references/000048_upstream-copy.md) | The rules of a different repository are an unchanged copy | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/references/000049](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/references/000049_upstream-applies.md) | Each rule of a different repository applies unless a project rule replaces it | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/references/000050](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/references/000050_no-contradiction.md) | A rule of the project does not contradict a rule of a different repository | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/references/000082](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/references/000082_lock-file.md) | spezi.lock holds the commit and the hash of each copy | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/references/000092](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/references/000092_transitive-copy.md) | A copy brings the upstreams of its repository | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/structures/000033](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/structures/000033_whole-structure.md) | A structure spec shows one structure as one diagram | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/structures/000034](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/structures/000034_mermaid-diagram.md) | The diagram is one Mermaid block of a fixed type | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/structures/000035](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/structures/000035_elements-table.md) | Each element of the diagram has a row in the element table | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/structures/000036](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/structures/000036_element-path.md) | An element names the code that holds it | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/structures/000037](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/structures/000037_diagram-size.md) | A diagram has at most 25 elements | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/structures/000038](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/structures/000038_diagram-follows-code.md) | A change of the structure changes the diagram | approved |
| [github.com/frederikbeimgraben/spezi:C/specs/structures/000039](/specs/.upstream/github.com/frederikbeimgraben/spezi/conventions/specs/structures/000039_structures-key.md) | A rule names the structures that it uses | approved |
| [github.com/frederikbeimgraben/spezi:F/cli/add/000068](/specs/.upstream/github.com/frederikbeimgraben/spezi/requirements/functional/cli/add/000068_add-copy.md) | spezi add adds the copy of a different repository | approved |
| [github.com/frederikbeimgraben/spezi:F/cli/agents/000079](/specs/.upstream/github.com/frederikbeimgraben/spezi/requirements/functional/cli/agents/000079_agents-file.md) | spezi writes the rules for agents to AGENTS.md | approved |
| [github.com/frederikbeimgraben/spezi:F/cli/check/000065](/specs/.upstream/github.com/frederikbeimgraben/spezi/requirements/functional/cli/check/000065_check-specs.md) | spezi check checks the specs | approved |
| [github.com/frederikbeimgraben/spezi:F/cli/configure/000086](/specs/.upstream/github.com/frederikbeimgraben/spezi/requirements/functional/cli/configure/000086_configure.md) | spezi configure changes the settings in spezi.toml | approved |
| [github.com/frederikbeimgraben/spezi:F/cli/init/000066](/specs/.upstream/github.com/frederikbeimgraben/spezi/requirements/functional/cli/init/000066_install-kit.md) | spezi init adds the kit to a project | approved |
| [github.com/frederikbeimgraben/spezi:F/cli/install/000083](/specs/.upstream/github.com/frederikbeimgraben/spezi/requirements/functional/cli/install/000083_install.md) | spezi install brings a project to the state of its settings | approved |
| [github.com/frederikbeimgraben/spezi:F/cli/list/000072](/specs/.upstream/github.com/frederikbeimgraben/spezi/requirements/functional/cli/list/000072_list-specs.md) | spezi list prints every rule | approved |
| [github.com/frederikbeimgraben/spezi:F/cli/lsp/000088](/specs/.upstream/github.com/frederikbeimgraben/spezi/requirements/functional/cli/lsp/000088_language-server.md) | spezi lsp runs the language server | approved |
| [github.com/frederikbeimgraben/spezi:F/cli/mcp/000074](/specs/.upstream/github.com/frederikbeimgraben/spezi/requirements/functional/cli/mcp/000074_mcp-server.md) | spezi mcp runs the MCP server | approved |
| [github.com/frederikbeimgraben/spezi:F/cli/migrate/000081](/specs/.upstream/github.com/frederikbeimgraben/spezi/requirements/functional/cli/migrate/000081_migrations.md) | spezi migrates a project and its copies to a new kit | approved |
| [github.com/frederikbeimgraben/spezi:F/cli/new/000069](/specs/.upstream/github.com/frederikbeimgraben/spezi/requirements/functional/cli/new/000069_new-spec.md) | spezi new makes a new spec from its template | approved |
| [github.com/frederikbeimgraben/spezi:F/cli/output/000076](/specs/.upstream/github.com/frederikbeimgraben/spezi/requirements/functional/cli/output/000076_formatted-output.md) | spezi formats its output for a terminal | approved |
| [github.com/frederikbeimgraben/spezi:F/cli/output/000077](/specs/.upstream/github.com/frederikbeimgraben/spezi/requirements/functional/cli/output/000077_changed-files.md) | spezi lists the files that a command changes | approved |
| [github.com/frederikbeimgraben/spezi:F/cli/output/000080](/specs/.upstream/github.com/frederikbeimgraben/spezi/requirements/functional/cli/output/000080_json-output.md) | spezi prints its data as JSON | approved |
| [github.com/frederikbeimgraben/spezi:F/cli/questions/000085](/specs/.upstream/github.com/frederikbeimgraben/spezi/requirements/functional/cli/questions/000085_questions.md) | init, add and update ask questions on a terminal | approved |
| [github.com/frederikbeimgraben/spezi:F/cli/remove/000087](/specs/.upstream/github.com/frederikbeimgraben/spezi/requirements/functional/cli/remove/000087_remove.md) | spezi remove removes the copy of a different repository | approved |
| [github.com/frederikbeimgraben/spezi:F/cli/resolve/000070](/specs/.upstream/github.com/frederikbeimgraben/spezi/requirements/functional/cli/resolve/000070_resolve-id.md) | spezi resolve prints the long form of an ID | approved |
| [github.com/frederikbeimgraben/spezi:F/cli/search/000073](/specs/.upstream/github.com/frederikbeimgraben/spezi/requirements/functional/cli/search/000073_search-specs.md) | spezi search finds rules by a text | approved |
| [github.com/frederikbeimgraben/spezi:F/cli/settings/000078](/specs/.upstream/github.com/frederikbeimgraben/spezi/requirements/functional/cli/settings/000078_settings.md) | spezi.toml holds the settings of the spezi command | approved |
| [github.com/frederikbeimgraben/spezi:F/cli/settings/000084](/specs/.upstream/github.com/frederikbeimgraben/spezi/requirements/functional/cli/settings/000084_feature-switches.md) | spezi.toml switches the optional parts of the kit on and off | approved |
| [github.com/frederikbeimgraben/spezi:F/cli/setup-ide/000089](/specs/.upstream/github.com/frederikbeimgraben/spezi/requirements/functional/cli/setup-ide/000089_setup-ide.md) | spezi setup-ide adds the language server to Zed or VS Code | approved |
| [github.com/frederikbeimgraben/spezi:F/cli/show/000071](/specs/.upstream/github.com/frederikbeimgraben/spezi/requirements/functional/cli/show/000071_show-spec.md) | spezi show prints the full text of a spec | approved |
| [github.com/frederikbeimgraben/spezi:F/cli/update/000067](/specs/.upstream/github.com/frederikbeimgraben/spezi/requirements/functional/cli/update/000067_update-copy.md) | spezi update resolves the refs again and replaces the copies | approved |
| [github.com/frederikbeimgraben/spezi:S/shared/functional/000052](/specs/.upstream/github.com/frederikbeimgraben/spezi/style/shared/functional/000052_body-shape.md) | A function body has one shape | approved |
| [github.com/frederikbeimgraben/spezi:S/shared/functional/000053](/specs/.upstream/github.com/frederikbeimgraben/spezi/style/shared/functional/000053_readability-limit.md) | Readability limits the single expression | approved |
| [github.com/frederikbeimgraben/spezi:S/shared/functional/000054](/specs/.upstream/github.com/frederikbeimgraben/spezi/style/shared/functional/000054_bind-once.md) | A local is bound once | approved |
| [github.com/frederikbeimgraben/spezi:S/shared/functional/000055](/specs/.upstream/github.com/frederikbeimgraben/spezi/style/shared/functional/000055_no-mutation.md) | A value is not mutated | approved |
| [github.com/frederikbeimgraben/spezi:S/shared/functional/000056](/specs/.upstream/github.com/frederikbeimgraben/spezi/style/shared/functional/000056_comprehensions.md) | Comprehensions instead of loops | approved |
| [github.com/frederikbeimgraben/spezi:S/shared/functional/000057](/specs/.upstream/github.com/frederikbeimgraben/spezi/style/shared/functional/000057_exhaustive-match.md) | A branch on one value is an exhaustive match | approved |
| [github.com/frederikbeimgraben/spezi:S/shared/functional/000058](/specs/.upstream/github.com/frederikbeimgraben/spezi/style/shared/functional/000058_frozen-data.md) | Data types are frozen by default | approved |
| [github.com/frederikbeimgraben/spezi:S/shared/functional/000059](/specs/.upstream/github.com/frederikbeimgraben/spezi/style/shared/functional/000059_exceptions.md) | The exceptions of the functional style are named | approved |
| [github.com/frederikbeimgraben/spezi:U/specs/lifecycle/000041](/specs/.upstream/github.com/frederikbeimgraben/spezi/structures/specs/lifecycle/000041_status-life-cycle.md) | The status of a spec moves from draft to approved, replaced or removed | approved |
| [github.com/frederikbeimgraben/spezi:U/specs/model/000040](/specs/.upstream/github.com/frederikbeimgraben/spezi/structures/specs/model/000040_spec-model.md) | A spec has a front matter, a body and links to other specs | approved |
| [github.com/frederikbeimgraben/spezi:W/kit/migrations/000090](/specs/.upstream/github.com/frederikbeimgraben/spezi/workflow/kit/migrations/000090_migration-ci.md) | The CI migrates demo projects from each migration | approved |
| [github.com/frederikbeimgraben/spezi:W/kit/release/000091](/specs/.upstream/github.com/frederikbeimgraben/spezi/workflow/kit/release/000091_release-workflow.md) | A tag publishes the package and the binaries | approved |
| [github.com/frederikbeimgraben/spezi:W/specs/process/000001](/specs/.upstream/github.com/frederikbeimgraben/spezi/workflow/specs/process/000001_precedence.md) | A spec wins over other guidance | approved |
| [github.com/frederikbeimgraben/spezi:W/specs/process/000002](/specs/.upstream/github.com/frederikbeimgraben/spezi/workflow/specs/process/000002_spec-first.md) | A change request starts as a spec | approved |
| [github.com/frederikbeimgraben/spezi:W/specs/process/000003](/specs/.upstream/github.com/frederikbeimgraben/spezi/workflow/specs/process/000003_change-process.md) | A change goes through a pull request | approved |
