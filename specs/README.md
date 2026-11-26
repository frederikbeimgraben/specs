# Specs

The binding rules of this project. One file holds one rule. A protocol spec holds one whole data
format. A structure spec holds one UML diagram in Mermaid. The rules for specs are in
[conventions/specs/](conventions/specs/) and [workflow/specs/](workflow/specs/). Copy a template to start a new spec:

- [TEMPLATE.md](TEMPLATE.md) for a functional, non-functional, style, convention, workflow or agent rule.
- [TEMPLATE-protocol.md](TEMPLATE-protocol.md) for a protocol spec.
- [TEMPLATE-structure.md](TEMPLATE-structure.md) for a structure spec.
- [TEMPLATE-decision.md](TEMPLATE-decision.md) for a decision spec.

Run `python3 scripts/check_specs.py --write` after each change. It writes the tree and the index.

## Tree

```
specs/
  structures/
    specs/  lifecycle, model
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
| [A/work/approval/000045](agents/work/approval/000045_one-spec-per-question.md) | An agent asks for the approval of one spec in one question | approved |
| [A/work/approval/000046](agents/work/approval/000046_show-the-whole-spec.md) | An agent shows the whole spec for its approval | approved |
| [A/work/questions/000043](agents/work/questions/000043_ask-each-detail.md) | An agent asks the user about each open detail | approved |
| [A/work/questions/000044](agents/work/questions/000044_follow-the-spec.md) | To follow a spec is not an assumption | approved |
| [C/specs/content/000018](conventions/specs/content/000018_only-the-rule.md) | A spec contains only the rule | approved |
| [C/specs/content/000019](conventions/specs/content/000019_one-thing.md) | One rule controls one thing | approved |
| [C/specs/content/000020](conventions/specs/content/000020_examinable.md) | A rule can be examined | approved |
| [C/specs/content/000021](conventions/specs/content/000021_must-and-must-not.md) | The rule text uses must and must not | approved |
| [C/specs/content/000022](conventions/specs/content/000022_reason.md) | A rule gives its reason | approved |
| [C/specs/content/000023](conventions/specs/content/000023_test.md) | A rule names its test | approved |
| [C/specs/content/000024](conventions/specs/content/000024_current-rule.md) | A spec states the current rule | approved |
| [C/specs/content/000025](conventions/specs/content/000025_ste.md) | A spec is written in ASD-STE100 | approved |
| [C/specs/content/000026](conventions/specs/content/000026_product-terms.md) | Product terms stay as the product shows them | approved |
| [C/specs/decisions/000042](conventions/specs/decisions/000042_whole-decision.md) | A decision spec records one decision with its alternatives | approved |
| [C/specs/format/000008](conventions/specs/format/000008_copy-the-template.md) | A new spec starts as a copy of the template | approved |
| [C/specs/format/000009](conventions/specs/format/000009_front-matter.md) | A spec starts with a YAML front matter | approved |
| [C/specs/format/000010](conventions/specs/format/000010_status.md) | The status shows the approval | approved |
| [C/specs/format/000011](conventions/specs/format/000011_one-rule-per-file.md) | One file holds one rule | approved |
| [C/specs/format/000012](conventions/specs/format/000012_rule-id.md) | The rule ID has kind, path and number | approved |
| [C/specs/format/000013](conventions/specs/format/000013_unique-number.md) | The number is the identity of a rule | approved |
| [C/specs/format/000014](conventions/specs/format/000014_moved-rule.md) | A moved rule keeps its number | approved |
| [C/specs/format/000015](conventions/specs/format/000015_labels.md) | Labels in a rule are fixed | approved |
| [C/specs/format/000016](conventions/specs/format/000016_file-name.md) | The file name is number and name | approved |
| [C/specs/format/000017](conventions/specs/format/000017_section-sign-reference.md) | Code refers to a rule with the § sign | approved |
| [C/specs/layout/000004](conventions/specs/layout/000004_tree.md) | The tree sorts by kind, then by area and topic | approved |
| [C/specs/layout/000005](conventions/specs/layout/000005_folder-names.md) | Folder names are lower case kebab case | approved |
| [C/specs/layout/000006](conventions/specs/layout/000006_one-place.md) | A rule is written in one place | approved |
| [C/specs/layout/000007](conventions/specs/layout/000007_index.md) | The index lists every rule | approved |
| [C/specs/protocols/000027](conventions/specs/protocols/000027_whole-format.md) | A protocol spec describes one whole format | approved |
| [C/specs/protocols/000028](conventions/specs/protocols/000028_schema-file.md) | A JSON format has a JSON Schema file beside its spec | approved |
| [C/specs/protocols/000029](conventions/specs/protocols/000029_checked-example.md) | The example of a JSON format matches its schema | approved |
| [C/specs/protocols/000030](conventions/specs/protocols/000030_breaking-change.md) | A breaking change of a format is a new protocol spec | approved |
| [C/specs/protocols/000031](conventions/specs/protocols/000031_code-against-schema.md) | A test checks the output of the code against the schema | approved |
| [C/specs/protocols/000032](conventions/specs/protocols/000032_protocols-key.md) | A rule names the formats that it uses | approved |
| [C/specs/references/000047](conventions/specs/references/000047_foreign-reference.md) | A reference to a rule of a different repository names the repository | approved |
| [C/specs/references/000048](conventions/specs/references/000048_upstream-copy.md) | The rules of a different repository are an unchanged copy | approved |
| [C/specs/references/000049](conventions/specs/references/000049_upstream-applies.md) | Each rule of a different repository applies unless a project rule replaces it | approved |
| [C/specs/references/000050](conventions/specs/references/000050_no-contradiction.md) | A rule of the project does not contradict a rule of a different repository | approved |
| [C/specs/structures/000033](conventions/specs/structures/000033_whole-structure.md) | A structure spec shows one structure as one diagram | approved |
| [C/specs/structures/000034](conventions/specs/structures/000034_mermaid-diagram.md) | The diagram is one Mermaid block of a fixed type | approved |
| [C/specs/structures/000035](conventions/specs/structures/000035_elements-table.md) | Each element of the diagram has a row in the element table | approved |
| [C/specs/structures/000036](conventions/specs/structures/000036_element-path.md) | An element names the code that holds it | approved |
| [C/specs/structures/000037](conventions/specs/structures/000037_diagram-size.md) | A diagram has at most 25 elements | approved |
| [C/specs/structures/000038](conventions/specs/structures/000038_diagram-follows-code.md) | A change of the structure changes the diagram | approved |
| [C/specs/structures/000039](conventions/specs/structures/000039_structures-key.md) | A rule names the structures that it uses | approved |
| [U/specs/lifecycle/000041](structures/specs/lifecycle/000041_status-life-cycle.md) | The status of a spec moves from draft to approved, replaced or removed | approved |
| [U/specs/model/000040](structures/specs/model/000040_spec-model.md) | A spec has a front matter, a body and links to other specs | approved |
| [W/specs/process/000001](workflow/specs/process/000001_precedence.md) | A spec wins over other guidance | approved |
| [W/specs/process/000002](workflow/specs/process/000002_spec-first.md) | A change request starts as a spec | approved |
| [W/specs/process/000003](workflow/specs/process/000003_change-process.md) | A change goes through a pull request | approved |
