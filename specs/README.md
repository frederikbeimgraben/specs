# Specs

The binding rules of this project. `specs/` holds only the rules of the
project. The command `specs check --write` writes this file to
`.specs/index.md` and to `specs/README.md`. Do not change these files by hand
(000007).

A new spec starts with
`specs new <kind> <area>/<topic> <name> "<title>"` (000008).

## Tree

```
specs/
  requirements/
    functional/
      cli/  add, check, init, list, mcp, new, output, resolve, search, show, update
  structures/
    specs/  lifecycle, model
  style/
    python/  docs, functional, lint, typing, version
    shared/  functional
  conventions/
    specs/  content, decisions, format, layout, protocols, references, structures
  workflow/
    specs/  process
  agents/
    work/  approval, questions
```

## Index

| ID | Title | Status |
| --- | --- | --- |
| [A/work/approval/000045](/specs/agents/work/approval/000045_one-spec-per-question.md) | An agent asks for the approval of one spec in one question | approved |
| [A/work/approval/000046](/specs/agents/work/approval/000046_show-the-whole-spec.md) | An agent shows the whole spec for its approval | approved |
| [A/work/questions/000043](/specs/agents/work/questions/000043_ask-each-detail.md) | An agent asks the user about each open detail | approved |
| [A/work/questions/000044](/specs/agents/work/questions/000044_follow-the-spec.md) | To follow a spec is not an assumption | approved |
| [C/specs/content/000018](/specs/conventions/specs/content/000018_only-the-rule.md) | A spec contains only the rule | approved |
| [C/specs/content/000019](/specs/conventions/specs/content/000019_one-thing.md) | One rule controls one thing | approved |
| [C/specs/content/000020](/specs/conventions/specs/content/000020_examinable.md) | A rule can be examined | approved |
| [C/specs/content/000021](/specs/conventions/specs/content/000021_must-and-must-not.md) | The rule text uses must and must not | approved |
| [C/specs/content/000022](/specs/conventions/specs/content/000022_reason.md) | A rule gives its reason | approved |
| [C/specs/content/000023](/specs/conventions/specs/content/000023_test.md) | A rule names its test | approved |
| [C/specs/content/000024](/specs/conventions/specs/content/000024_current-rule.md) | A spec states the current rule | approved |
| [C/specs/content/000025](/specs/conventions/specs/content/000025_ste.md) | A spec is written in ASD-STE100 | approved |
| [C/specs/content/000026](/specs/conventions/specs/content/000026_product-terms.md) | Product terms stay as the product shows them | approved |
| [C/specs/decisions/000042](/specs/conventions/specs/decisions/000042_whole-decision.md) | A decision spec records one decision with its alternatives | approved |
| [C/specs/format/000008](/specs/conventions/specs/format/000008_copy-the-template.md) | A new spec starts as a copy of the template | approved |
| [C/specs/format/000009](/specs/conventions/specs/format/000009_front-matter.md) | A spec starts with a YAML front matter | approved |
| [C/specs/format/000010](/specs/conventions/specs/format/000010_status.md) | The status shows the approval | approved |
| [C/specs/format/000011](/specs/conventions/specs/format/000011_one-rule-per-file.md) | One file holds one rule | approved |
| [C/specs/format/000012](/specs/conventions/specs/format/000012_rule-id.md) | The rule ID has kind, path and number | approved |
| [C/specs/format/000013](/specs/conventions/specs/format/000013_unique-number.md) | The number is the identity of a rule | approved |
| [C/specs/format/000014](/specs/conventions/specs/format/000014_moved-rule.md) | A moved rule keeps its number | approved |
| [C/specs/format/000015](/specs/conventions/specs/format/000015_labels.md) | Labels in a rule are fixed | approved |
| [C/specs/format/000016](/specs/conventions/specs/format/000016_file-name.md) | The file name is number and name | approved |
| [C/specs/format/000017](/specs/conventions/specs/format/000017_section-sign-reference.md) | Code refers to a rule with the § sign | approved |
| [C/specs/layout/000004](/specs/conventions/specs/layout/000004_tree.md) | The tree sorts by kind, then by area and topic | approved |
| [C/specs/layout/000005](/specs/conventions/specs/layout/000005_folder-names.md) | Folder names are lower case kebab case | approved |
| [C/specs/layout/000006](/specs/conventions/specs/layout/000006_one-place.md) | A rule is written in one place | approved |
| [C/specs/layout/000007](/specs/conventions/specs/layout/000007_index.md) | The index lists every rule | approved |
| [C/specs/layout/000051](/specs/conventions/specs/layout/000051_project-rules-only.md) | specs/ holds only the rules of the project | approved |
| [C/specs/protocols/000027](/specs/conventions/specs/protocols/000027_whole-format.md) | A protocol spec describes one whole format | approved |
| [C/specs/protocols/000028](/specs/conventions/specs/protocols/000028_schema-file.md) | A JSON format has a JSON Schema file beside its spec | approved |
| [C/specs/protocols/000029](/specs/conventions/specs/protocols/000029_checked-example.md) | The example of a JSON format matches its schema | approved |
| [C/specs/protocols/000030](/specs/conventions/specs/protocols/000030_breaking-change.md) | A breaking change of a format is a new protocol spec | approved |
| [C/specs/protocols/000031](/specs/conventions/specs/protocols/000031_code-against-schema.md) | A test checks the output of the code against the schema | approved |
| [C/specs/protocols/000032](/specs/conventions/specs/protocols/000032_protocols-key.md) | A rule names the formats that it uses | approved |
| [C/specs/references/000047](/specs/conventions/specs/references/000047_foreign-reference.md) | A reference to a rule of a different repository names the repository | approved |
| [C/specs/references/000048](/specs/conventions/specs/references/000048_upstream-copy.md) | The rules of a different repository are an unchanged copy | approved |
| [C/specs/references/000049](/specs/conventions/specs/references/000049_upstream-applies.md) | Each rule of a different repository applies unless a project rule replaces it | approved |
| [C/specs/references/000050](/specs/conventions/specs/references/000050_no-contradiction.md) | A rule of the project does not contradict a rule of a different repository | approved |
| [C/specs/structures/000033](/specs/conventions/specs/structures/000033_whole-structure.md) | A structure spec shows one structure as one diagram | approved |
| [C/specs/structures/000034](/specs/conventions/specs/structures/000034_mermaid-diagram.md) | The diagram is one Mermaid block of a fixed type | approved |
| [C/specs/structures/000035](/specs/conventions/specs/structures/000035_elements-table.md) | Each element of the diagram has a row in the element table | approved |
| [C/specs/structures/000036](/specs/conventions/specs/structures/000036_element-path.md) | An element names the code that holds it | approved |
| [C/specs/structures/000037](/specs/conventions/specs/structures/000037_diagram-size.md) | A diagram has at most 25 elements | approved |
| [C/specs/structures/000038](/specs/conventions/specs/structures/000038_diagram-follows-code.md) | A change of the structure changes the diagram | approved |
| [C/specs/structures/000039](/specs/conventions/specs/structures/000039_structures-key.md) | A rule names the structures that it uses | approved |
| [F/cli/add/000068](/specs/requirements/functional/cli/add/000068_add-copy.md) | specs add adds the copy of a different repository | approved |
| [F/cli/check/000065](/specs/requirements/functional/cli/check/000065_check-specs.md) | specs check checks the specs and writes the index | approved |
| [F/cli/init/000066](/specs/requirements/functional/cli/init/000066_install-kit.md) | specs init adds the kit to a project | approved |
| [F/cli/list/000072](/specs/requirements/functional/cli/list/000072_list-specs.md) | specs list prints every rule | approved |
| [F/cli/mcp/000074](/specs/requirements/functional/cli/mcp/000074_mcp-server.md) | specs mcp runs the MCP server | approved |
| [F/cli/new/000069](/specs/requirements/functional/cli/new/000069_new-spec.md) | specs new makes a new spec from its template | approved |
| [F/cli/output/000076](/specs/requirements/functional/cli/output/000076_formatted-output.md) | specs formats its output for a terminal | approved |
| [F/cli/resolve/000070](/specs/requirements/functional/cli/resolve/000070_resolve-id.md) | specs resolve prints the long form of an ID | approved |
| [F/cli/search/000073](/specs/requirements/functional/cli/search/000073_search-specs.md) | specs search finds rules by a text | approved |
| [F/cli/show/000071](/specs/requirements/functional/cli/show/000071_show-spec.md) | specs show prints the full text of a spec | approved |
| [F/cli/update/000067](/specs/requirements/functional/cli/update/000067_update-copy.md) | specs update replaces a copy and its ref | draft |
| [S/python/docs/000062](/specs/style/python/docs/000062_docstrings.md) | Python code is documented in Google-style docstrings | approved |
| [S/python/functional/000063](/specs/style/python/functional/000063_python-means.md) | Python code uses fixed means for the functional style | approved |
| [S/python/lint/000064](/specs/style/python/lint/000064_ruff-clean.md) | ruff reports no warning | approved |
| [S/python/lint/000075](/specs/style/python/lint/000075_ruff-format.md) | ruff format changes nothing | approved |
| [S/python/typing/000061](/specs/style/python/typing/000061_strict-types.md) | Python code is strictly typed | approved |
| [S/python/version/000060](/specs/style/python/version/000060_python-313.md) | Python code needs Python 3.13 or later | approved |
| [S/shared/functional/000052](/specs/style/shared/functional/000052_body-shape.md) | A function body has one shape | approved |
| [S/shared/functional/000053](/specs/style/shared/functional/000053_readability-limit.md) | Readability limits the single expression | approved |
| [S/shared/functional/000054](/specs/style/shared/functional/000054_bind-once.md) | A local is bound once | approved |
| [S/shared/functional/000055](/specs/style/shared/functional/000055_no-mutation.md) | A value is not mutated | approved |
| [S/shared/functional/000056](/specs/style/shared/functional/000056_comprehensions.md) | Comprehensions instead of loops | approved |
| [S/shared/functional/000057](/specs/style/shared/functional/000057_exhaustive-match.md) | A branch on one value is an exhaustive match | approved |
| [S/shared/functional/000058](/specs/style/shared/functional/000058_frozen-data.md) | Data types are frozen by default | approved |
| [S/shared/functional/000059](/specs/style/shared/functional/000059_exceptions.md) | The exceptions of the functional style are named | approved |
| [U/specs/lifecycle/000041](/specs/structures/specs/lifecycle/000041_status-life-cycle.md) | The status of a spec moves from draft to approved, replaced or removed | approved |
| [U/specs/model/000040](/specs/structures/specs/model/000040_spec-model.md) | A spec has a front matter, a body and links to other specs | approved |
| [W/specs/process/000001](/specs/workflow/specs/process/000001_precedence.md) | A spec wins over other guidance | approved |
| [W/specs/process/000002](/specs/workflow/specs/process/000002_spec-first.md) | A change request starts as a spec | approved |
| [W/specs/process/000003](/specs/workflow/specs/process/000003_change-process.md) | A change goes through a pull request | approved |

## Upstream

The rules of different repositories that apply to this project (000049).

No rules.
