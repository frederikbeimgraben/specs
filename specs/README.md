# Specs

The binding rules of this project. The kind folders of `specs/` hold the rules
of the project, `specs/.upstream/` the rules of different repositories and
`specs/.templates/` the templates. The command `spezi install` writes this
file. Do not change it by hand (spec 000007).

A new spec starts with
`spezi new <kind> <area>/<topic> <name> "<title>" --scope <path>` (spec 000008).

## Tree

```
specs/
  requirements/
    functional/
      cli/  add, agents, check, configure, init, install, list, lsp, mcp, migrate, new, output, questions, remove, resolve, search, settings, setup-ide, show, update
    non-functional/
      cli/  startup
  structures/
    specs/  lifecycle, model
  conventions/
    specs/  content, decisions, format, layout, protocols, references, structures
  workflow/
    kit/    migrations, release, tests
    specs/  process
  agents/
    work/  approval, questions
  .upstream/
    github.com/frederikbeimgraben/spezi-functional/
    github.com/frederikbeimgraben/spezi-python/
```

## Index

| ID | Title | Status |
| --- | --- | --- |
| [A/work/approval/000045](/specs/agents/work/approval/000045_one-spec-per-question.md) | An agent asks for the approval of one spec in one question | approved |
| [A/work/approval/000046](/specs/agents/work/approval/000046_show-the-whole-spec.md) | An agent shows the whole spec for its approval | approved |
| [A/work/questions/000043](/specs/agents/work/questions/000043_ask-each-detail.md) | An agent asks the user about each open detail | approved |
| [A/work/questions/000044](/specs/agents/work/questions/000044_follow-the-spec.md) | To follow a spec is not an assumption | approved |
| [A/work/questions/000345](/specs/agents/work/questions/000345_one-detail-per-question.md) | An agent asks about one detail in one question | approved |
| [C/specs/content/000018](/specs/conventions/specs/content/000018_only-the-rule.md) | A spec contains only the rule | approved |
| [C/specs/content/000019](/specs/conventions/specs/content/000019_one-thing.md) | One rule controls one thing | approved |
| [C/specs/content/000020](/specs/conventions/specs/content/000020_examinable.md) | A rule can be examined | approved |
| [C/specs/content/000021](/specs/conventions/specs/content/000021_must-and-must-not.md) | The rule text uses must and must not | approved |
| [C/specs/content/000022](/specs/conventions/specs/content/000022_reason.md) | A rule gives its reason | approved |
| [C/specs/content/000023](/specs/conventions/specs/content/000023_test.md) | A rule names its test | approved |
| [C/specs/content/000024](/specs/conventions/specs/content/000024_current-rule.md) | A spec states the current rule | approved |
| [C/specs/content/000025](/specs/conventions/specs/content/000025_ste.md) | A spec is written in ASD-STE100 | approved |
| [C/specs/content/000026](/specs/conventions/specs/content/000026_product-terms.md) | Product terms stay as the product shows them | approved |
| [C/specs/content/000097](/specs/conventions/specs/content/000097_present-tense-facts.md) | A fact in a rule is in the present tense | approved |
| [C/specs/content/000098](/specs/conventions/specs/content/000098_short-keeps-reason.md) | A shorter version of a rule keeps the cause | approved |
| [C/specs/content/000099](/specs/conventions/specs/content/000099_unit-tests-key.md) | The unit tests of a rule are in tests | approved |
| [C/specs/content/000100](/specs/conventions/specs/content/000100_dates.md) | A spec shows a date only when the rule depends on it | approved |
| [C/specs/content/000101](/specs/conventions/specs/content/000101_no-tickets.md) | A spec does not refer to tickets, pull requests or threads | approved |
| [C/specs/content/000102](/specs/conventions/specs/content/000102_english.md) | A spec is in English | approved |
| [C/specs/content/000103](/specs/conventions/specs/content/000103_instruction-length.md) | An instruction has at most 20 words | approved |
| [C/specs/content/000104](/specs/conventions/specs/content/000104_description-length.md) | A description has at most 25 words | approved |
| [C/specs/content/000105](/specs/conventions/specs/content/000105_active-voice.md) | A spec uses the active voice | approved |
| [C/specs/content/000106](/specs/conventions/specs/content/000106_one-instruction.md) | One sentence holds one instruction | approved |
| [C/specs/content/000107](/specs/conventions/specs/content/000107_one-word.md) | A spec uses one word for one thing | approved |
| [C/specs/content/000108](/specs/conventions/specs/content/000108_no-ing.md) | A spec uses no -ing form as a noun or an adjective | approved |
| [C/specs/content/000346](/specs/conventions/specs/content/000346_measurable-words.md) | A rule gives a value for a quality word | approved |
| [C/specs/decisions/000042](/specs/conventions/specs/decisions/000042_whole-decision.md) | A decision spec has fixed sections | approved |
| [C/specs/decisions/000109](/specs/conventions/specs/decisions/000109_one-decision.md) | A decision spec records one decision | approved |
| [C/specs/format/000008](/specs/conventions/specs/format/000008_copy-the-template.md) | A new spec starts as a copy of the template | approved |
| [C/specs/format/000009](/specs/conventions/specs/format/000009_front-matter.md) | A spec starts with a YAML front matter | approved |
| [C/specs/format/000010](/specs/conventions/specs/format/000010_status.md) | The status shows the approval | approved |
| [C/specs/format/000011](/specs/conventions/specs/format/000011_one-rule-per-file.md) | One file holds one rule | approved |
| [C/specs/format/000012](/specs/conventions/specs/format/000012_rule-id.md) | The rule ID has kind, path and number | approved |
| [C/specs/format/000013](/specs/conventions/specs/format/000013_unique-number.md) | The number is the identity of a rule | approved |
| [C/specs/format/000014](/specs/conventions/specs/format/000014_moved-rule.md) | A moved rule keeps its number | approved |
| [C/specs/format/000015](/specs/conventions/specs/format/000015_labels.md) | Labels in a rule are fixed | approved |
| [C/specs/format/000016](/specs/conventions/specs/format/000016_file-name.md) | The file name is number and name | approved |
| [C/specs/format/000017](/specs/conventions/specs/format/000017_spec-reference.md) | Code refers to a rule with (spec <number>) | approved |
| [C/specs/format/000110](/specs/conventions/specs/format/000110_copy-with-new.md) | spezi new makes the copy of the template | approved |
| [C/specs/format/000111](/specs/conventions/specs/format/000111_front-matter-block.md) | A spec starts with a front matter block | approved |
| [C/specs/format/000112](/specs/conventions/specs/format/000112_valid-yaml.md) | The front matter is valid YAML | approved |
| [C/specs/format/000113](/specs/conventions/specs/format/000113_no-other-keys.md) | The front matter has no other keys | approved |
| [C/specs/format/000114](/specs/conventions/specs/format/000114_paths-exist.md) | Each path of the front matter exists | approved |
| [C/specs/format/000115](/specs/conventions/specs/format/000115_no-body-metadata.md) | The body holds no metadata | approved |
| [C/specs/format/000116](/specs/conventions/specs/format/000116_approval-in-words.md) | An agent sets approved only after the approval in words | approved |
| [C/specs/format/000117](/specs/conventions/specs/format/000117_replaced-is-named.md) | A replaced rule is in replaces of a rule in force | approved |
| [C/specs/format/000118](/specs/conventions/specs/format/000118_replaced-by-list.md) | replaced_by lists each rule that replaces the rule | approved |
| [C/specs/format/000119](/specs/conventions/specs/format/000119_body-order.md) | The body has the title, the rule text and the labels | approved |
| [C/specs/format/000120](/specs/conventions/specs/format/000120_no-other-headings.md) | A spec uses no other headings | approved |
| [C/specs/format/000121](/specs/conventions/specs/format/000121_id-from-path.md) | The file does not hold the rule ID | approved |
| [C/specs/format/000122](/specs/conventions/specs/format/000122_next-number.md) | A new rule gets the highest number plus one | approved |
| [C/specs/format/000123](/specs/conventions/specs/format/000123_renumber-on-conflict.md) | The later pull request gives its specs new numbers | approved |
| [C/specs/format/000124](/specs/conventions/specs/format/000124_never-reuse.md) | A number is never used again | approved |
| [C/specs/format/000125](/specs/conventions/specs/format/000125_move-references.md) | A move changes every reference in the same pull request | approved |
| [C/specs/format/000126](/specs/conventions/specs/format/000126_label-paragraph.md) | A label starts its own paragraph | approved |
| [C/specs/format/000127](/specs/conventions/specs/format/000127_labels-last.md) | The labels come after the rule text and the sections | approved |
| [C/specs/format/000128](/specs/conventions/specs/format/000128_reference-list.md) | One reference can hold a list of rules | approved |
| [C/specs/format/000129](/specs/conventions/specs/format/000129_no-range.md) | A reference holds no range of numbers | approved |
| [C/specs/format/000130](/specs/conventions/specs/format/000130_no-bare-number.md) | A Markdown file has no rule number outside a reference | approved |
| [C/specs/format/000199](/specs/conventions/specs/format/000199_new-key-same-pr.md) | A new key of the front matter changes the model in the same pull request | approved |
| [C/specs/format/000200](/specs/conventions/specs/format/000200_no-way-back.md) | A replaced or removed spec stays out of force | approved |
| [C/specs/format/000201](/specs/conventions/specs/format/000201_comeback-new-spec.md) | A rule that comes back gets a new spec | approved |
| [C/specs/layout/000004](/specs/conventions/specs/layout/000004_tree.md) | The tree sorts by kind, then by area and topic | approved |
| [C/specs/layout/000005](/specs/conventions/specs/layout/000005_folder-names.md) | Folder names are lower case kebab case | approved |
| [C/specs/layout/000006](/specs/conventions/specs/layout/000006_one-place.md) | A rule is written in one place | approved |
| [C/specs/layout/000007](/specs/conventions/specs/layout/000007_index.md) | The index lists every rule | approved |
| [C/specs/layout/000051](/specs/conventions/specs/layout/000051_project-rules-only.md) | specs/ holds the rules of the project and the files of the kit | approved |
| [C/specs/layout/000131](/specs/conventions/specs/layout/000131_kind-order.md) | A rule goes to the first kind that applies | approved |
| [C/specs/layout/000132](/specs/conventions/specs/layout/000132_area-topic.md) | Below the kind folder are the area and the topic | approved |
| [C/specs/layout/000133](/specs/conventions/specs/layout/000133_topic-folder.md) | A rule is in the topic folder that it controls | approved |
| [C/specs/layout/000134](/specs/conventions/specs/layout/000134_owning-area.md) | A rule for two areas is in the area that owns the code | approved |
| [C/specs/layout/000135](/specs/conventions/specs/layout/000135_index-copies.md) | The index lists the rules of the copies | approved |
| [C/specs/layout/000136](/specs/conventions/specs/layout/000136_index-not-by-hand.md) | Nobody changes the index by hand | approved |
| [C/specs/layout/000137](/specs/conventions/specs/layout/000137_index-in-pr.md) | A pull request with a new rule updates the index | approved |
| [C/specs/protocols/000027](/specs/conventions/specs/protocols/000027_whole-format.md) | A protocol spec has fixed sections | approved |
| [C/specs/protocols/000028](/specs/conventions/specs/protocols/000028_schema-file.md) | A JSON format has a JSON Schema file beside its spec | approved |
| [C/specs/protocols/000029](/specs/conventions/specs/protocols/000029_checked-example.md) | The example of a JSON format matches its schema | approved |
| [C/specs/protocols/000030](/specs/conventions/specs/protocols/000030_breaking-change.md) | A breaking change of a format is a new protocol spec | approved |
| [C/specs/protocols/000031](/specs/conventions/specs/protocols/000031_code-against-schema.md) | A test checks the output of the code against the schema | approved |
| [C/specs/protocols/000032](/specs/conventions/specs/protocols/000032_protocols-key.md) | A rule names the formats that it uses | approved |
| [C/specs/protocols/000138](/specs/conventions/specs/protocols/000138_one-format.md) | A protocol spec describes one format | approved |
| [C/specs/protocols/000139](/specs/conventions/specs/protocols/000139_format-in-one-spec.md) | One format is in one protocol spec | approved |
| [C/specs/protocols/000140](/specs/conventions/specs/protocols/000140_schema-dialect.md) | A schema uses JSON Schema 2020-12 | approved |
| [C/specs/protocols/000141](/specs/conventions/specs/protocols/000141_schema-by-hand.md) | A person writes the schema file | approved |
| [C/specs/protocols/000142](/specs/conventions/specs/protocols/000142_no-schema-for-other.md) | A format that is not JSON has no schema file | approved |
| [C/specs/protocols/000143](/specs/conventions/specs/protocols/000143_schema-table.md) | A format that is not JSON has a table in Schema | approved |
| [C/specs/protocols/000144](/specs/conventions/specs/protocols/000144_json-is-schema.md) | Each JSON file below protocols is a schema file | approved |
| [C/specs/protocols/000145](/specs/conventions/specs/protocols/000145_example-matches-schema.md) | A JSON example matches its schema | approved |
| [C/specs/protocols/000146](/specs/conventions/specs/protocols/000146_version-number.md) | The version of a format is a whole number from 1 | approved |
| [C/specs/protocols/000147](/specs/conventions/specs/protocols/000147_compatible-in-place.md) | A compatible change keeps the spec and its version | approved |
| [C/specs/protocols/000148](/specs/conventions/specs/protocols/000148_old-format-replaced.md) | The old format is replaced when the product drops it | approved |
| [C/specs/protocols/000149](/specs/conventions/specs/protocols/000149_compatible-changes.md) | Only two changes of a format are compatible | approved |
| [C/specs/protocols/000150](/specs/conventions/specs/protocols/000150_test-makes-format.md) | The test makes the format with the code | approved |
| [C/specs/protocols/000151](/specs/conventions/specs/protocols/000151_test-reads-fixture.md) | The test of a read format validates its fixture | approved |
| [C/specs/protocols/000152](/specs/conventions/specs/protocols/000152_no-empty-protocols.md) | A spec without a format has no key protocols | approved |
| [C/specs/protocols/000153](/specs/conventions/specs/protocols/000153_protocols-in-force.md) | Each entry of protocols is in force | approved |
| [C/specs/references/000047](/specs/conventions/specs/references/000047_foreign-reference.md) | A reference to a rule of a different repository names the repository | approved |
| [C/specs/references/000048](/specs/conventions/specs/references/000048_upstream-copy.md) | The rules of a different repository are an unchanged copy | draft |
| [C/specs/references/000049](/specs/conventions/specs/references/000049_upstream-applies.md) | Each rule of a different repository applies unless a project rule replaces it | draft |
| [C/specs/references/000050](/specs/conventions/specs/references/000050_no-contradiction.md) | A rule of the project does not contradict a rule of a different repository | approved |
| [C/specs/references/000082](/specs/conventions/specs/references/000082_lock-file.md) | spezi.lock holds the commit and the hash of each copy | approved |
| [C/specs/references/000092](/specs/conventions/specs/references/000092_transitive-copy.md) | A copy brings the upstreams of its repository | approved |
| [C/specs/references/000154](/specs/conventions/specs/references/000154_same-repo-number.md) | A reference to a rule of the same repository is the number | approved |
| [C/specs/references/000155](/specs/conventions/specs/references/000155_short-form.md) | Code, front matter and spec text use the short form | approved |
| [C/specs/references/000156](/specs/conventions/specs/references/000156_reference-in-force.md) | A reference names a rule in force | approved |
| [C/specs/references/000157](/specs/conventions/specs/references/000157_include-limits.md) | include limits the copy to its folders | approved |
| [C/specs/references/000158](/specs/conventions/specs/references/000158_include-folder-form.md) | A folder of include is a path of kebab-case folders | approved |
| [C/specs/references/000159](/specs/conventions/specs/references/000159_own-left-out.md) | A copy leaves out the own folders of its repository | approved |
| [C/specs/references/000160](/specs/conventions/specs/references/000160_include-wins.md) | include wins over own | approved |
| [C/specs/references/000161](/specs/conventions/specs/references/000161_no-hidden-folders.md) | A copy leaves out the hidden folders | approved |
| [C/specs/references/000162](/specs/conventions/specs/references/000162_migrated-copy.md) | A copy of an older kit holds the migrated rules | approved |
| [C/specs/references/000163](/specs/conventions/specs/references/000163_copy-not-by-hand.md) | Nobody changes a file of a copy by hand | approved |
| [C/specs/references/000164](/specs/conventions/specs/references/000164_copy-commands.md) | Only these commands change a copy | approved |
| [C/specs/references/000165](/specs/conventions/specs/references/000165_gitattributes-line.md) | gitattributes keeps the line ends of the copies | approved |
| [C/specs/references/000166](/specs/conventions/specs/references/000166_install-adds-line.md) | spezi install adds the line to gitattributes | approved |
| [C/specs/references/000167](/specs/conventions/specs/references/000167_keep-line.md) | No command removes the line of gitattributes | approved |
| [C/specs/references/000168](/specs/conventions/specs/references/000168_replace-upstream-rule.md) | A project rule replaces a rule of a copy that must not apply | draft |
| [C/specs/references/000169](/specs/conventions/specs/references/000169_drop-with-decision.md) | A decision spec drops a rule of a copy | approved |
| [C/specs/references/000170](/specs/conventions/specs/references/000170_no-reference-to-replaced.md) | A reference does not point to a replaced rule | approved |
| [C/specs/references/000171](/specs/conventions/specs/references/000171_report-contradiction.md) | An agent reports a contradiction to the owner | approved |
| [C/specs/references/000172](/specs/conventions/specs/references/000172_ref-form.md) | ref names a tag, a branch or a commit | approved |
| [C/specs/references/000173](/specs/conventions/specs/references/000173_lock-writers.md) | Only five commands write spezi.lock | approved |
| [C/specs/references/000174](/specs/conventions/specs/references/000174_lock-not-by-hand.md) | Nobody changes spezi.lock by hand | approved |
| [C/specs/references/000175](/specs/conventions/specs/references/000175_lock-check.md) | spezi check finds a lock that does not agree | approved |
| [C/specs/references/000176](/specs/conventions/specs/references/000176_transitive-cases.md) | Each repository of transitive gets a copy or a skip | approved |
| [C/specs/references/000177](/specs/conventions/specs/references/000177_direct-copy-lock.md) | The copy of a direct upstream holds its spezi.lock | approved |
| [C/specs/references/000178](/specs/conventions/specs/references/000178_transitive-no-lock.md) | The copy of a transitive upstream holds no spezi.lock | approved |
| [C/specs/references/000179](/specs/conventions/specs/references/000179_include-union.md) | One commit of a transitive upstream gives the union of include | approved |
| [C/specs/references/000180](/specs/conventions/specs/references/000180_commit-conflict.md) | Two commits of a transitive upstream are an error | approved |
| [C/specs/references/000181](/specs/conventions/specs/references/000181_direct-table-wins.md) | A direct table removes the conflict of two commits | approved |
| [C/specs/references/000182](/specs/conventions/specs/references/000182_transitive-same-rules.md) | A copy of a transitive upstream follows the copy rules | approved |
| [C/specs/references/000183](/specs/conventions/specs/references/000183_transitive-commands.md) | Only init, add and update change transitive | approved |
| [C/specs/structures/000033](/specs/conventions/specs/structures/000033_whole-structure.md) | A structure spec has fixed sections | approved |
| [C/specs/structures/000034](/specs/conventions/specs/structures/000034_mermaid-diagram.md) | The diagram is one Mermaid block of a fixed type | approved |
| [C/specs/structures/000035](/specs/conventions/specs/structures/000035_elements-table.md) | Each element of the diagram has a row in the element table | approved |
| [C/specs/structures/000036](/specs/conventions/specs/structures/000036_element-path.md) | An element names the code that holds it | approved |
| [C/specs/structures/000037](/specs/conventions/specs/structures/000037_diagram-size.md) | A diagram has at most 25 elements | approved |
| [C/specs/structures/000038](/specs/conventions/specs/structures/000038_diagram-follows-code.md) | A change of the structure changes the diagram | approved |
| [C/specs/structures/000039](/specs/conventions/specs/structures/000039_structures-key.md) | A rule names the structures that it uses | approved |
| [C/specs/structures/000184](/specs/conventions/specs/structures/000184_one-structure.md) | A structure spec shows one structure | approved |
| [C/specs/structures/000185](/specs/conventions/specs/structures/000185_structure-in-one-spec.md) | One structure is in one structure spec | approved |
| [C/specs/structures/000186](/specs/conventions/specs/structures/000186_binding-property.md) | A structure spec names the property that binds the code | approved |
| [C/specs/structures/000187](/specs/conventions/specs/structures/000187_diagram-type.md) | The first line of the diagram names its type | approved |
| [C/specs/structures/000188](/specs/conventions/specs/structures/000188_no-styles.md) | The diagram holds no styles | approved |
| [C/specs/structures/000189](/specs/conventions/specs/structures/000189_row-name.md) | A row names one element with its name in the diagram | approved |
| [C/specs/structures/000190](/specs/conventions/specs/structures/000190_row-for-each-element.md) | Each element of the diagram has a row | approved |
| [C/specs/structures/000191](/specs/conventions/specs/structures/000191_meaning-sentence.md) | Meaning tells in one sentence what the element is | approved |
| [C/specs/structures/000192](/specs/conventions/specs/structures/000192_path-exists.md) | The path of an element exists | approved |
| [C/specs/structures/000193](/specs/conventions/specs/structures/000193_path-dash.md) | An element without code has the path - | approved |
| [C/specs/structures/000194](/specs/conventions/specs/structures/000194_paths-in-implementation.md) | A structure spec lists its element paths in implementation | approved |
| [C/specs/structures/000195](/specs/conventions/specs/structures/000195_diagram-shows-code.md) | A diagram shows the code as it is | approved |
| [C/specs/structures/000196](/specs/conventions/specs/structures/000196_planned-structure.md) | A planned structure is a draft without implementation | approved |
| [C/specs/structures/000197](/specs/conventions/specs/structures/000197_no-empty-structures.md) | A spec without a structure has no key structures | approved |
| [C/specs/structures/000198](/specs/conventions/specs/structures/000198_structures-in-force.md) | Each entry of structures is in force | approved |
| [F/cli/add/000068](/specs/requirements/functional/cli/add/000068_add-copy.md) | spezi add adds the copy of a different repository | approved |
| [F/cli/add/000303](/specs/requirements/functional/cli/add/000303_default-ref.md) | Without a ref, spezi add takes the highest version | approved |
| [F/cli/add/000304](/specs/requirements/functional/cli/add/000304_repo-name.md) | A repository name has a host and one or more groups | approved |
| [F/cli/add/000305](/specs/requirements/functional/cli/add/000305_add-include.md) | spezi add copies only the chosen folders | approved |
| [F/cli/add/000306](/specs/requirements/functional/cli/add/000306_include-no-nested.md) | include holds no folder below a different folder of include | approved |
| [F/cli/add/000307](/specs/requirements/functional/cli/add/000307_add-stops.md) | spezi add stops for a known repository or a missing folder | approved |
| [F/cli/add/000308](/specs/requirements/functional/cli/add/000308_add-transitive.md) | spezi add copies the chosen transitive upstreams | approved |
| [F/cli/agents/000079](/specs/requirements/functional/cli/agents/000079_agents-file.md) | spezi writes the rules for agents to AGENTS.md | approved |
| [F/cli/agents/000271](/specs/requirements/functional/cli/agents/000271_block-markers.md) | The block starts and ends with a marker line | approved |
| [F/cli/agents/000272](/specs/requirements/functional/cli/agents/000272_block-content.md) | The block holds the approved A and W rules | approved |
| [F/cli/agents/000273](/specs/requirements/functional/cli/agents/000273_block-keeps-text.md) | The text around the block stays | approved |
| [F/cli/agents/000274](/specs/requirements/functional/cli/agents/000274_block-current.md) | spezi check finds a block that is not current | approved |
| [F/cli/agents/000275](/specs/requirements/functional/cli/agents/000275_claude-file.md) | spezi init writes CLAUDE.md | approved |
| [F/cli/agents/000276](/specs/requirements/functional/cli/agents/000276_claude-file-kept.md) | spezi init keeps a CLAUDE.md without the import | approved |
| [F/cli/agents/000277](/specs/requirements/functional/cli/agents/000277_old-markers.md) | A migration gives an old block the new markers | approved |
| [F/cli/check/000065](/specs/requirements/functional/cli/check/000065_check-specs.md) | spezi check checks the specs | approved |
| [F/cli/check/000093](/specs/requirements/functional/cli/check/000093_check-ste.md) | spezi check checks the rules of ASD-STE100 | approved |
| [F/cli/check/000094](/specs/requirements/functional/cli/check/000094_own-references.md) | spezi check finds a reference to a rule of own in a file for projects | approved |
| [F/cli/check/000209](/specs/requirements/functional/cli/check/000209_check-copies-agree.md) | spezi check checks the settings, the lock and the copies | approved |
| [F/cli/check/000210](/specs/requirements/functional/cli/check/000210_check-references.md) | spezi check checks each reference to a rule | approved |
| [F/cli/check/000211](/specs/requirements/functional/cli/check/000211_check-unreadable-copy.md) | spezi check reports a rule of a copy that it cannot read | approved |
| [F/cli/check/000212](/specs/requirements/functional/cli/check/000212_check-copy-conventions.md) | spezi check runs no convention check on a copy | approved |
| [F/cli/check/000213](/specs/requirements/functional/cli/check/000213_check-line-order.md) | spezi check prints the errors before the warnings | approved |
| [F/cli/check/000214](/specs/requirements/functional/cli/check/000214_check-count-line.md) | The last line of spezi check counts the rules and the findings | approved |
| [F/cli/check/000215](/specs/requirements/functional/cli/check/000215_check-error-line.md) | An error line names the path and the line | approved |
| [F/cli/check/000216](/specs/requirements/functional/cli/check/000216_check-path-line.md) | An error of a folder names only the path | approved |
| [F/cli/check/000217](/specs/requirements/functional/cli/check/000217_check-exit-code.md) | spezi check exits with 1 for an error | approved |
| [F/cli/check/000218](/specs/requirements/functional/cli/check/000218_check-no-write.md) | spezi check changes no file | approved |
| [F/cli/check/000219](/specs/requirements/functional/cli/check/000219_check-offline.md) | spezi check needs no network | approved |
| [F/cli/check/000338](/specs/requirements/functional/cli/check/000338_ste-not-copies.md) | The check of ASD-STE100 skips the copies | approved |
| [F/cli/check/000339](/specs/requirements/functional/cli/check/000339_ste-switch.md) | ste = false turns off the check of ASD-STE100 | approved |
| [F/cli/check/000340](/specs/requirements/functional/cli/check/000340_ste-prose.md) | The check of ASD-STE100 reads only the prose | approved |
| [F/cli/check/000341](/specs/requirements/functional/cli/check/000341_ste-words.md) | A word and a sentence have fixed limits | approved |
| [F/cli/check/000342](/specs/requirements/functional/cli/check/000342_ste-lists.md) | The word lists come from the reference skill | approved |
| [F/cli/check/000343](/specs/requirements/functional/cli/check/000343_ste-warning-line.md) | A warning line names the path and the line | approved |
| [F/cli/check/000344](/specs/requirements/functional/cli/check/000344_ste-exit-code.md) | A warning does not change the exit code | approved |
| [F/cli/configure/000086](/specs/requirements/functional/cli/configure/000086_configure.md) | spezi configure changes the settings in spezi.toml | approved |
| [F/cli/configure/000264](/specs/requirements/functional/cli/configure/000264_menu-loop.md) | The menu comes back after each item | approved |
| [F/cli/configure/000265](/specs/requirements/functional/cli/configure/000265_menu-save.md) | save writes spezi.toml when the settings are correct | approved |
| [F/cli/configure/000266](/specs/requirements/functional/cli/configure/000266_menu-discard.md) | discard and Ctrl+C stop without a change | approved |
| [F/cli/configure/000267](/specs/requirements/functional/cli/configure/000267_configure-key.md) | spezi configure sets one key without questions | approved |
| [F/cli/configure/000268](/specs/requirements/functional/cli/configure/000268_configure-bad-value.md) | spezi configure stops for a bad key or value | approved |
| [F/cli/configure/000269](/specs/requirements/functional/cli/configure/000269_configure-no-terminal.md) | spezi configure needs a terminal or a key | approved |
| [F/cli/configure/000270](/specs/requirements/functional/cli/configure/000270_configure-keeps-text.md) | spezi configure keeps the other text of spezi.toml | approved |
| [F/cli/init/000066](/specs/requirements/functional/cli/init/000066_install-kit.md) | spezi init adds the kit to a project | approved |
| [F/cli/init/000283](/specs/requirements/functional/cli/init/000283_init-ci.md) | The CI job runs spezi check | approved |
| [F/cli/init/000284](/specs/requirements/functional/cli/init/000284_init-devshell.md) | spezi init gives the project a devShell | approved |
| [F/cli/init/000285](/specs/requirements/functional/cli/init/000285_flake-input.md) | The flake input spezi names the commit of the lock | approved |
| [F/cli/init/000286](/specs/requirements/functional/cli/init/000286_flake-no-follows.md) | The input spezi does not follow nixpkgs | approved |
| [F/cli/init/000287](/specs/requirements/functional/cli/init/000287_init-forge.md) | spezi init proposes the forge of the remote | approved |
| [F/cli/init/000288](/specs/requirements/functional/cli/init/000288_init-stops.md) | spezi init stops in five cases | approved |
| [F/cli/install/000083](/specs/requirements/functional/cli/install/000083_install.md) | spezi install brings a project to the state of its settings | approved |
| [F/cli/install/000289](/specs/requirements/functional/cli/install/000289_transitive-hints.md) | spezi install tells each new and each changed transitive upstream | approved |
| [F/cli/install/000290](/specs/requirements/functional/cli/install/000290_mcp-json-stop.md) | spezi install stops for a broken .mcp.json | approved |
| [F/cli/install/000291](/specs/requirements/functional/cli/install/000291_install-offline.md) | spezi install of a current project needs no network | approved |
| [F/cli/install/000292](/specs/requirements/functional/cli/install/000292_end-steps.md) | Five commands end with the steps of spezi install | approved |
| [F/cli/install/000293](/specs/requirements/functional/cli/install/000293_older-program.md) | An older program stops the command | approved |
| [F/cli/list/000072](/specs/requirements/functional/cli/list/000072_list-specs.md) | spezi list prints every rule | approved |
| [F/cli/list/000227](/specs/requirements/functional/cli/list/000227_list-kind.md) | spezi list with a kind prints only this kind | approved |
| [F/cli/list/000228](/specs/requirements/functional/cli/list/000228_list-unknown-kind.md) | spezi list stops for an unknown kind | approved |
| [F/cli/list/000229](/specs/requirements/functional/cli/list/000229_list-line.md) | A line of spezi list has four columns | approved |
| [F/cli/list/000230](/specs/requirements/functional/cli/list/000230_list-mcp-kind.md) | The MCP tool list takes an optional kind | approved |
| [F/cli/lsp/000088](/specs/requirements/functional/cli/lsp/000088_language-server.md) | spezi lsp runs the language server | approved |
| [F/cli/lsp/000322](/specs/requirements/functional/cli/lsp/000322_lsp-diagnostics.md) | The language server shows each finding of the check | approved |
| [F/cli/lsp/000323](/specs/requirements/functional/cli/lsp/000323_lsp-line-one.md) | A finding without a line goes to line 1 | approved |
| [F/cli/lsp/000324](/specs/requirements/functional/cli/lsp/000324_lsp-check-times.md) | The language server checks at three times | approved |
| [F/cli/lsp/000325](/specs/requirements/functional/cli/lsp/000325_lsp-reference.md) | A reference in the editor is a rule ID or a spec reference | approved |
| [F/cli/lsp/000326](/specs/requirements/functional/cli/lsp/000326_lsp-hover.md) | The hover shows the rule | approved |
| [F/cli/lsp/000327](/specs/requirements/functional/cli/lsp/000327_lsp-definition.md) | The definition opens the spec | approved |
| [F/cli/lsp/000328](/specs/requirements/functional/cli/lsp/000328_lsp-range.md) | The hover marks only the rule ID | approved |
| [F/cli/lsp/000329](/specs/requirements/functional/cli/lsp/000329_lsp-no-write.md) | The language server writes no file | approved |
| [F/cli/mcp/000074](/specs/requirements/functional/cli/mcp/000074_mcp-server.md) | spezi mcp runs the MCP server | approved |
| [F/cli/mcp/000233](/specs/requirements/functional/cli/mcp/000233_mcp-same-result.md) | An MCP tool gives the result of its command | approved |
| [F/cli/mcp/000234](/specs/requirements/functional/cli/mcp/000234_mcp-configure.md) | The MCP tool configure takes a key and a value | approved |
| [F/cli/mcp/000235](/specs/requirements/functional/cli/mcp/000235_mcp-read-only-tools.md) | Five MCP tools write no file | approved |
| [F/cli/mcp/000236](/specs/requirements/functional/cli/mcp/000236_mcp-plain.md) | The MCP server returns plain text | approved |
| [F/cli/migrate/000081](/specs/requirements/functional/cli/migrate/000081_migrations.md) | spezi migrates a project and its copies to a new kit | approved |
| [F/cli/migrate/000278](/specs/requirements/functional/cli/migrate/000278_migration-once.md) | A migration changes only the old format | approved |
| [F/cli/migrate/000279](/specs/requirements/functional/cli/migrate/000279_migration-order.md) | A command runs each migration that a ref does not hold | approved |
| [F/cli/migrate/000280](/specs/requirements/functional/cli/migrate/000280_old-name.md) | The command reads the files of the old name | approved |
| [F/cli/migrate/000281](/specs/requirements/functional/cli/migrate/000281_newer-kit.md) | A copy that needs a newer kit stops the command | approved |
| [F/cli/migrate/000282](/specs/requirements/functional/cli/migrate/000282_migrated-line.md) | Each migration that ran gives one line | approved |
| [F/cli/new/000069](/specs/requirements/functional/cli/new/000069_new-spec.md) | spezi new makes a new spec from its template | approved |
| [F/cli/new/000220](/specs/requirements/functional/cli/new/000220_new-number.md) | spezi new gives the next free number | approved |
| [F/cli/new/000221](/specs/requirements/functional/cli/new/000221_new-keys.md) | spezi new fills the front matter | approved |
| [F/cli/new/000222](/specs/requirements/functional/cli/new/000222_new-scope.md) | spezi new needs a scope that exists | approved |
| [F/cli/new/000223](/specs/requirements/functional/cli/new/000223_new-owner.md) | spezi new takes the owner from the option or from git | approved |
| [F/cli/new/000224](/specs/requirements/functional/cli/new/000224_new-schema.md) | spezi new writes a schema for a JSON protocol | approved |
| [F/cli/new/000225](/specs/requirements/functional/cli/new/000225_new-mcp-scope.md) | The MCP tool new takes the scope as a list | approved |
| [F/cli/output/000076](/specs/requirements/functional/cli/output/000076_formatted-output.md) | spezi formats its output for a terminal | approved |
| [F/cli/output/000077](/specs/requirements/functional/cli/output/000077_changed-files.md) | spezi lists the files that a command changes | approved |
| [F/cli/output/000080](/specs/requirements/functional/cli/output/000080_json-output.md) | spezi prints its data as JSON | approved |
| [F/cli/output/000237](/specs/requirements/functional/cli/output/000237_count-line-color.md) | The color of the count line tells the result | approved |
| [F/cli/output/000238](/specs/requirements/functional/cli/output/000238_raw-plain.md) | Raw output is plain text | approved |
| [F/cli/output/000239](/specs/requirements/functional/cli/output/000239_help-color.md) | The help has color | approved |
| [F/cli/output/000240](/specs/requirements/functional/cli/output/000240_help-plain.md) | The help has color only on a terminal | approved |
| [F/cli/output/000241](/specs/requirements/functional/cli/output/000241_list-place.md) | The list of files comes before the report of the check | approved |
| [F/cli/output/000242](/specs/requirements/functional/cli/output/000242_list-sorted-relative.md) | The list of files is sorted by relative path | approved |
| [F/cli/output/000243](/specs/requirements/functional/cli/output/000243_record-each-write.md) | Each write of a file goes to the list | approved |
| [F/cli/output/000244](/specs/requirements/functional/cli/output/000244_same-content.md) | A write with the same content is no change | approved |
| [F/cli/output/000245](/specs/requirements/functional/cli/output/000245_copied-folder.md) | A copied folder lists only its changed files | approved |
| [F/cli/output/000246](/specs/requirements/functional/cli/output/000246_mcp-changed.md) | The MCP tools return the list of files | approved |
| [F/cli/output/000247](/specs/requirements/functional/cli/output/000247_raw-json.md) | --json and --raw do not go together | approved |
| [F/cli/output/000248](/specs/requirements/functional/cli/output/000248_rule-object.md) | A rule object has six keys | approved |
| [F/cli/output/000249](/specs/requirements/functional/cli/output/000249_error-object.md) | An error object has four keys | approved |
| [F/cli/output/000250](/specs/requirements/functional/cli/output/000250_changed-object.md) | An object of changed has a mark and a path | approved |
| [F/cli/output/000251](/specs/requirements/functional/cli/output/000251_json-stop.md) | A stop with --json gives an error object | approved |
| [F/cli/output/000252](/specs/requirements/functional/cli/output/000252_json-path.md) | A path in JSON is relative | approved |
| [F/cli/questions/000085](/specs/requirements/functional/cli/questions/000085_questions.md) | init, add and update ask questions on a terminal | approved |
| [F/cli/questions/000311](/specs/requirements/functional/cli/questions/000311_show-proposal.md) | Each question shows its proposal | approved |
| [F/cli/questions/000312](/specs/requirements/functional/cli/questions/000312_argument-wins.md) | A value of the command line replaces its question | approved |
| [F/cli/questions/000313](/specs/requirements/functional/cli/questions/000313_no-terminal.md) | Without a terminal, each question takes its proposal | approved |
| [F/cli/questions/000314](/specs/requirements/functional/cli/questions/000314_risk-stops.md) | A question with a risk stops a command without a terminal | approved |
| [F/cli/questions/000315](/specs/requirements/functional/cli/questions/000315_ctrl-c.md) | Ctrl+C stops the questions with an error | approved |
| [F/cli/questions/000316](/specs/requirements/functional/cli/questions/000316_init-questions.md) | The questions of spezi init | approved |
| [F/cli/questions/000317](/specs/requirements/functional/cli/questions/000317_add-questions.md) | The questions of spezi add | approved |
| [F/cli/questions/000318](/specs/requirements/functional/cli/questions/000318_update-questions.md) | The questions of spezi update | approved |
| [F/cli/questions/000319](/specs/requirements/functional/cli/questions/000319_run-question.md) | A command asks Run? before each copy | approved |
| [F/cli/questions/000320](/specs/requirements/functional/cli/questions/000320_run-summary.md) | The summary shows the answers or the changed rules | approved |
| [F/cli/questions/000321](/specs/requirements/functional/cli/questions/000321_init-no-write-before-run.md) | spezi init writes no file before Run? | approved |
| [F/cli/remove/000087](/specs/requirements/functional/cli/remove/000087_remove.md) | spezi remove removes the copy of a different repository | approved |
| [F/cli/remove/000309](/specs/requirements/functional/cli/remove/000309_remove-keeps-lines.md) | spezi remove keeps the other lines of spezi.toml | approved |
| [F/cli/remove/000310](/specs/requirements/functional/cli/remove/000310_remove-stops.md) | spezi remove stops for the kit and for an unknown repository | approved |
| [F/cli/resolve/000070](/specs/requirements/functional/cli/resolve/000070_resolve-id.md) | spezi resolve prints the long form of an ID | approved |
| [F/cli/resolve/000226](/specs/requirements/functional/cli/resolve/000226_unknown-id.md) | resolve and show stop for an unknown ID | approved |
| [F/cli/search/000073](/specs/requirements/functional/cli/search/000073_search-specs.md) | spezi search finds rules by a text | approved |
| [F/cli/search/000231](/specs/requirements/functional/cli/search/000231_search-case.md) | spezi search ignores the case | approved |
| [F/cli/search/000232](/specs/requirements/functional/cli/search/000232_queries-no-write.md) | A query writes no file | approved |
| [F/cli/settings/000078](/specs/requirements/functional/cli/settings/000078_settings.md) | spezi.toml holds the settings of the spezi command | approved |
| [F/cli/settings/000084](/specs/requirements/functional/cli/settings/000084_feature-switches.md) | spezi.toml switches the optional parts of the kit on and off | approved |
| [F/cli/settings/000253](/specs/requirements/functional/cli/settings/000253_template-no-comment.md) | The template of spezi.toml has no comment | approved |
| [F/cli/settings/000254](/specs/requirements/functional/cli/settings/000254_old-comments.md) | A migration removes the comments of an old template | approved |
| [F/cli/settings/000255](/specs/requirements/functional/cli/settings/000255_bad-settings.md) | A bad setting stops each command | approved |
| [F/cli/settings/000256](/specs/requirements/functional/cli/settings/000256_no-switch.md) | The index, the copies and the templates have no switch | approved |
| [F/cli/settings/000257](/specs/requirements/functional/cli/settings/000257_write-only-on.md) | A command writes only the parts that are on | approved |
| [F/cli/settings/000258](/specs/requirements/functional/cli/settings/000258_remove-off.md) | spezi install removes the parts that are off | approved |
| [F/cli/settings/000259](/specs/requirements/functional/cli/settings/000259_flake-off.md) | spezi update keeps flake.nix when flake is off | approved |
| [F/cli/settings/000260](/specs/requirements/functional/cli/settings/000260_ci-off.md) | With ci off, a command ignores the GitLab file | approved |
| [F/cli/settings/000261](/specs/requirements/functional/cli/settings/000261_agents-off.md) | With agents off, spezi check skips the block | approved |
| [F/cli/settings/000262](/specs/requirements/functional/cli/settings/000262_claude-needs-agents.md) | claude needs agents | approved |
| [F/cli/settings/000263](/specs/requirements/functional/cli/settings/000263_bad-switch.md) | An unknown switch is an error | approved |
| [F/cli/setup-ide/000089](/specs/requirements/functional/cli/setup-ide/000089_setup-ide.md) | spezi setup-ide adds the language server to Zed or VS Code | approved |
| [F/cli/setup-ide/000330](/specs/requirements/functional/cli/setup-ide/000330_ide-start.md) | The extension starts spezi lsp | approved |
| [F/cli/setup-ide/000331](/specs/requirements/functional/cli/setup-ide/000331_server-json.md) | server.json holds the program and the suffixes | approved |
| [F/cli/setup-ide/000332](/specs/requirements/functional/cli/setup-ide/000332_zed-languages.md) | Each suffix has its Zed language | approved |
| [F/cli/setup-ide/000333](/specs/requirements/functional/cli/setup-ide/000333_ide-rewrite.md) | spezi setup-ide writes the whole folder again | approved |
| [F/cli/setup-ide/000334](/specs/requirements/functional/cli/setup-ide/000334_ide-gitignore.md) | The editor folder goes to .gitignore | approved |
| [F/cli/setup-ide/000335](/specs/requirements/functional/cli/setup-ide/000335_code-install.md) | spezi setup-ide code offers to install the extension | approved |
| [F/cli/setup-ide/000336](/specs/requirements/functional/cli/setup-ide/000336_zed-install.md) | spezi setup-ide zed tells how to install the extension | approved |
| [F/cli/setup-ide/000337](/specs/requirements/functional/cli/setup-ide/000337_no-vsix.md) | spezi setup-ide code stops without spezi.vsix | approved |
| [F/cli/show/000071](/specs/requirements/functional/cli/show/000071_show-spec.md) | spezi show prints the full text of a spec | approved |
| [F/cli/update/000067](/specs/requirements/functional/cli/update/000067_update-copy.md) | spezi update resolves the refs again and replaces the copies | approved |
| [F/cli/update/000294](/specs/requirements/functional/cli/update/000294_update-include.md) | spezi update keeps include | approved |
| [F/cli/update/000295](/specs/requirements/functional/cli/update/000295_update-message.md) | spezi update gives one line for each repository | approved |
| [F/cli/update/000296](/specs/requirements/functional/cli/update/000296_update-transitive-lines.md) | spezi update gives one line for each transitive upstream | approved |
| [F/cli/update/000297](/specs/requirements/functional/cli/update/000297_update-transitive.md) | spezi update follows the new lock of a direct upstream | approved |
| [F/cli/update/000298](/specs/requirements/functional/cli/update/000298_update-kit-files.md) | spezi update of the kit replaces the kit files | approved |
| [F/cli/update/000299](/specs/requirements/functional/cli/update/000299_update-ide.md) | spezi update writes the editor folders again | approved |
| [F/cli/update/000300](/specs/requirements/functional/cli/update/000300_update-flake.md) | spezi update sets the flake input to the new commit | approved |
| [F/cli/update/000301](/specs/requirements/functional/cli/update/000301_update-shell-hint.md) | spezi update tells to load the devShell again | approved |
| [F/cli/update/000302](/specs/requirements/functional/cli/update/000302_update-stops.md) | spezi update stops in four cases | approved |
| [NF/cli/startup/000095](/specs/requirements/non-functional/cli/startup/000095_load-only-needed-libraries.md) | A command loads only the libraries that it needs | approved |
| [U/specs/lifecycle/000041](/specs/structures/specs/lifecycle/000041_status-life-cycle.md) | The status of a spec moves from draft to approved, replaced or removed | approved |
| [U/specs/model/000040](/specs/structures/specs/model/000040_spec-model.md) | A spec has a front matter, a body and links to other specs | approved |
| [W/kit/migrations/000090](/specs/workflow/kit/migrations/000090_migration-ci.md) | The CI migrates demo projects from each migration | approved |
| [W/kit/migrations/000203](/specs/workflow/kit/migrations/000203_start-commits.md) | The start commits come from the migrations | approved |
| [W/kit/migrations/000204](/specs/workflow/kit/migrations/000204_install-twice.md) | A migrated demo installs two times | approved |
| [W/kit/release/000091](/specs/workflow/kit/release/000091_release-workflow.md) | A tag publishes the package and the binaries | approved |
| [W/kit/release/000205](/specs/workflow/kit/release/000205_pr-builds-only.md) | A pull request builds and tests the release | approved |
| [W/kit/release/000206](/specs/workflow/kit/release/000206_publish-after-binaries.md) | The release publishes only after each binary passes | approved |
| [W/kit/release/000207](/specs/workflow/kit/release/000207_version-from-git.md) | The version comes from the git tag | approved |
| [W/kit/release/000208](/specs/workflow/kit/release/000208_flake-version.md) | The flake sets the version from the commit | approved |
| [W/kit/tests/000096](/specs/workflow/kit/tests/000096_parallel-tests.md) | The tests of the kit run in parallel | approved |
| [W/kit/tests/000347](/specs/workflow/kit/tests/000347_xdist-in-shell.md) | The development shell has pytest-xdist | approved |
| [W/kit/tests/000348](/specs/workflow/kit/tests/000348_test-isolation.md) | A test uses only its own files | approved |
| [W/specs/process/000001](/specs/workflow/specs/process/000001_precedence.md) | A spec wins over other guidance | approved |
| [W/specs/process/000002](/specs/workflow/specs/process/000002_spec-first.md) | A change request starts as a spec | approved |
| [W/specs/process/000003](/specs/workflow/specs/process/000003_change-process.md) | A change goes through a pull request | approved |
| [W/specs/process/000202](/specs/workflow/specs/process/000202_tell-the-owner.md) | An agent tells the owner when code and a spec do not agree | approved |

## Upstream

The rules of different repositories that apply to this project (spec 000049).

| ID | Title | Status |
| --- | --- | --- |
| [github.com/frederikbeimgraben/spezi-functional:S/shared/functional/000001](/specs/.upstream/github.com/frederikbeimgraben/spezi-functional/style/shared/functional/000001_body-shape.md) | A function body has one shape | approved |
| [github.com/frederikbeimgraben/spezi-functional:S/shared/functional/000002](/specs/.upstream/github.com/frederikbeimgraben/spezi-functional/style/shared/functional/000002_readability-limit.md) | An expression is at most three levels deep | approved |
| [github.com/frederikbeimgraben/spezi-functional:S/shared/functional/000003](/specs/.upstream/github.com/frederikbeimgraben/spezi-functional/style/shared/functional/000003_bind-once.md) | A local is bound once | approved |
| [github.com/frederikbeimgraben/spezi-functional:S/shared/functional/000004](/specs/.upstream/github.com/frederikbeimgraben/spezi-functional/style/shared/functional/000004_no-mutation.md) | A value is not mutated | approved |
| [github.com/frederikbeimgraben/spezi-functional:S/shared/functional/000005](/specs/.upstream/github.com/frederikbeimgraben/spezi-functional/style/shared/functional/000005_comprehensions.md) | Comprehensions instead of loops | approved |
| [github.com/frederikbeimgraben/spezi-functional:S/shared/functional/000006](/specs/.upstream/github.com/frederikbeimgraben/spezi-functional/style/shared/functional/000006_exhaustive-match.md) | A match is exhaustive | approved |
| [github.com/frederikbeimgraben/spezi-functional:S/shared/functional/000007](/specs/.upstream/github.com/frederikbeimgraben/spezi-functional/style/shared/functional/000007_frozen-data.md) | A data type is immutable | approved |
| [github.com/frederikbeimgraben/spezi-functional:S/shared/functional/000008](/specs/.upstream/github.com/frederikbeimgraben/spezi-functional/style/shared/functional/000008_exceptions.md) | The exceptions of the functional style are named | approved |
| [github.com/frederikbeimgraben/spezi-functional:S/shared/functional/000009](/specs/.upstream/github.com/frederikbeimgraben/spezi-functional/style/shared/functional/000009_readability-length.md) | An expression has at most 8 lines | approved |
| [github.com/frederikbeimgraben/spezi-functional:S/shared/functional/000010](/specs/.upstream/github.com/frederikbeimgraben/spezi-functional/style/shared/functional/000010_effect-loop.md) | A loop that only causes effects is a for statement | approved |
| [github.com/frederikbeimgraben/spezi-functional:S/shared/functional/000011](/specs/.upstream/github.com/frederikbeimgraben/spezi-functional/style/shared/functional/000011_match-from-three.md) | A branch with three or more outcomes is a match | approved |
| [github.com/frederikbeimgraben/spezi-functional:S/shared/functional/000012](/specs/.upstream/github.com/frederikbeimgraben/spezi-functional/style/shared/functional/000012_two-outcomes.md) | A branch with two outcomes is a conditional expression | approved |
| [github.com/frederikbeimgraben/spezi-functional:S/shared/functional/000013](/specs/.upstream/github.com/frederikbeimgraben/spezi-functional/style/shared/functional/000013_flat-conditional.md) | A conditional expression is nested at most one level | approved |
| [github.com/frederikbeimgraben/spezi-functional:S/shared/functional/000014](/specs/.upstream/github.com/frederikbeimgraben/spezi-functional/style/shared/functional/000014_frozen-fields.md) | The collection fields of a data type are immutable | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/docs/000003](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/docs/000003_docstrings.md) | Each module, class and function has a docstring | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/docs/000022](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/docs/000022_no-body-comments.md) | A function body holds no comment | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/errors/000011](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/errors/000011_base-exception.md) | A Python package has one base exception class | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/errors/000012](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/errors/000012_entry-point-catch.md) | The entry point catches only the base exception | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/errors/000034](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/errors/000034_exception-subclass.md) | Each exception class of a package is a subclass of its base exception | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/functional/000004](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/functional/000004_python-means.md) | Python code binds a local once | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/functional/000023](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/functional/000023_no-mutation-means.md) | Python code changes no value in place | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/functional/000024](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/functional/000024_comprehension-means.md) | Python code builds a value with a comprehension | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/functional/000025](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/functional/000025_assert-never.md) | A match that the type checker cannot see as exhaustive ends with assert_never | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/functional/000026](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/functional/000026_frozen-dataclass.md) | A Python data type is a frozen dataclass with slots | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/functional/000027](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/functional/000027_immutable-field-types.md) | A collection field has the type tuple, frozenset or Mapping | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/lint/000005](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/lint/000005_ruff-clean.md) | ruff reports no warning | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/lint/000006](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/lint/000006_ruff-format.md) | ruff format changes nothing | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/lint/000028](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/lint/000028_ruff-rules.md) | The rule selection of ruff holds these rules | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/lint/000029](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/lint/000029_explicit-selection.md) | The rule selection of ruff is an explicit list | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/lint/000030](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/lint/000030_noqa.md) | Code turns off a ruff rule only when it cannot obey it | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/naming/000017](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/naming/000017_private-names.md) | A name that a module does not export starts with _ | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/testing/000007](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/testing/000007_tests-folder.md) | Python tests are in tests/ | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/testing/000008](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/testing/000008_mirror-package.md) | tests/ mirrors the folders of a package with subpackages | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/testing/000009](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/testing/000009_test-functions.md) | A Python test is a function test_<behavior> | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/testing/000010](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/testing/000010_checked-tests.md) | The code checks also apply to the tests | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/testing/000031](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/testing/000031_test-file-names.md) | A Python test file has the name test_<topic>.py | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/testing/000032](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/testing/000032_assert-checks.md) | A Python test checks its result with assert | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/testing/000033](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/testing/000033_no-test-classes.md) | A Python test is not in a class | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/typing/000002](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/typing/000002_strict-types.md) | basedpyright reports no error | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/typing/000020](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/typing/000020_no-explicit-any.md) | Python code uses no explicit Any | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/typing/000021](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/typing/000021_closed-sets.md) | A closed set of values is an Enum or a Literal | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/version/000001](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/version/000001_python-313.md) | Python code needs Python 3.13 or later | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/version/000018](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/version/000018_ruff-target.md) | The target version of ruff is Python 3.13 | approved |
| [github.com/frederikbeimgraben/spezi-python:S/python/version/000019](/specs/.upstream/github.com/frederikbeimgraben/spezi-python/style/python/version/000019_basedpyright-target.md) | The Python version of basedpyright is 3.13 | approved |
