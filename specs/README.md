# Specs

The binding rules of this project. One file holds one rule. A protocol spec holds one whole data
format. A structure spec holds one UML diagram in Mermaid. The rules for specs are in
[style/specs/](style/specs/). Copy a template to start a new spec:

- [TEMPLATE.md](TEMPLATE.md) for a functional, non-functional or style rule.
- [TEMPLATE-protocol.md](TEMPLATE-protocol.md) for a protocol spec.
- [TEMPLATE-structure.md](TEMPLATE-structure.md) for a structure spec.

Run `python3 scripts/check_specs.py --write` after each change. It writes the tree and the index.

## Tree

```
specs/
  style/
    specs/  content, format, layout, protocols, structures
  structures/
    specs/  lifecycle, model
```

## Index

| ID | Title | Status |
| --- | --- | --- |
| [S/specs/content/000018](style/specs/content/000018_only-the-rule.md) | A spec contains only the rule | approved |
| [S/specs/content/000019](style/specs/content/000019_one-thing.md) | One rule controls one thing | approved |
| [S/specs/content/000020](style/specs/content/000020_examinable.md) | A rule can be examined | approved |
| [S/specs/content/000021](style/specs/content/000021_must-and-must-not.md) | The rule text uses must and must not | approved |
| [S/specs/content/000022](style/specs/content/000022_reason.md) | A rule gives its reason | approved |
| [S/specs/content/000023](style/specs/content/000023_test.md) | A rule names its test | approved |
| [S/specs/content/000024](style/specs/content/000024_current-rule.md) | A spec states the current rule | approved |
| [S/specs/content/000025](style/specs/content/000025_ste.md) | A spec is written in ASD-STE100 | approved |
| [S/specs/content/000026](style/specs/content/000026_product-terms.md) | Product terms stay as the product shows them | approved |
| [S/specs/format/000008](style/specs/format/000008_copy-the-template.md) | A new spec starts as a copy of the template | approved |
| [S/specs/format/000009](style/specs/format/000009_front-matter.md) | A spec starts with a YAML front matter | approved |
| [S/specs/format/000010](style/specs/format/000010_status.md) | The status shows the approval | approved |
| [S/specs/format/000011](style/specs/format/000011_one-rule-per-file.md) | One file holds one rule | approved |
| [S/specs/format/000012](style/specs/format/000012_rule-id.md) | The rule ID has kind, path and number | approved |
| [S/specs/format/000013](style/specs/format/000013_unique-number.md) | The number is the identity of a rule | approved |
| [S/specs/format/000014](style/specs/format/000014_moved-rule.md) | A moved rule keeps its number | approved |
| [S/specs/format/000015](style/specs/format/000015_labels.md) | Labels in a rule are fixed | approved |
| [S/specs/format/000016](style/specs/format/000016_file-name.md) | The file name is number and name | approved |
| [S/specs/format/000017](style/specs/format/000017_section-sign-reference.md) | Code refers to a rule with the § sign | approved |
| [S/specs/layout/000001](style/specs/layout/000001_precedence.md) | A spec wins over other guidance | approved |
| [S/specs/layout/000002](style/specs/layout/000002_spec-first.md) | A change request starts as a spec | approved |
| [S/specs/layout/000003](style/specs/layout/000003_change-process.md) | A change goes through a pull request | approved |
| [S/specs/layout/000004](style/specs/layout/000004_tree.md) | The tree sorts by kind, then by area and topic | approved |
| [S/specs/layout/000005](style/specs/layout/000005_folder-names.md) | Folder names are lower case kebab case | approved |
| [S/specs/layout/000006](style/specs/layout/000006_one-place.md) | A rule is written in one place | approved |
| [S/specs/layout/000007](style/specs/layout/000007_index.md) | The index lists every rule | approved |
| [S/specs/protocols/000027](style/specs/protocols/000027_whole-format.md) | A protocol spec describes one whole format | approved |
| [S/specs/protocols/000028](style/specs/protocols/000028_schema-file.md) | A JSON format has a JSON Schema file beside its spec | approved |
| [S/specs/protocols/000029](style/specs/protocols/000029_checked-example.md) | The example of a JSON format matches its schema | approved |
| [S/specs/protocols/000030](style/specs/protocols/000030_breaking-change.md) | A breaking change of a format is a new protocol spec | approved |
| [S/specs/protocols/000031](style/specs/protocols/000031_code-against-schema.md) | A test checks the output of the code against the schema | approved |
| [S/specs/protocols/000032](style/specs/protocols/000032_protocols-key.md) | A rule names the formats that it uses | approved |
| [S/specs/structures/000033](style/specs/structures/000033_whole-structure.md) | A structure spec shows one structure as one diagram | approved |
| [S/specs/structures/000034](style/specs/structures/000034_mermaid-diagram.md) | The diagram is one Mermaid block of a fixed type | approved |
| [S/specs/structures/000035](style/specs/structures/000035_elements-table.md) | Each element of the diagram has a row in the element table | approved |
| [S/specs/structures/000036](style/specs/structures/000036_element-path.md) | An element names the code that holds it | approved |
| [S/specs/structures/000037](style/specs/structures/000037_diagram-size.md) | A diagram has at most 25 elements | approved |
| [S/specs/structures/000038](style/specs/structures/000038_diagram-follows-code.md) | A change of the structure changes the diagram | approved |
| [S/specs/structures/000039](style/specs/structures/000039_structures-key.md) | A rule names the structures that it uses | approved |
| [U/specs/lifecycle/000041](structures/specs/lifecycle/000041_status-life-cycle.md) | The status of a spec moves from draft to approved, replaced or removed | approved |
| [U/specs/model/000040](structures/specs/model/000040_spec-model.md) | A spec has a front matter, a body and links to other specs | approved |
