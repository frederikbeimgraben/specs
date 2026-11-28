---
id: "000040"
title: A spec has a front matter, a body and links to other specs
kind: structure
status: approved
owner: frederikbeimgraben
updated: 2026-11-26
diagram: class
implementation:
  - src/spezi/project.py
  - specs/.templates/TEMPLATE.md
scope:
  - specs/
  - src/spezi/project.py
---

# A spec has a front matter, a body and links to other specs

The class `Spec` in `src/spezi/project.py` and the keys of the templates must agree with this
diagram. A new key of the front matter must change the diagram and the rule of the front matter (spec 000009) in the same pull
request.

## Diagram

```mermaid
classDiagram
  class Spec {
    +number: string
    +fullId: string
    +body: string
  }
  class FrontMatter {
    +title: string
    +owner: string
    +updated: date
    +implementation: list~string~
    +scope: list~string~
  }
  class Status {
    <<enumeration>>
    draft
    approved
    replaced
    removed
  }
  class Kind {
    <<enumeration>>
    functional
    non-functional
    protocol
    structure
    style
    convention
    workflow
    agent
    decision
  }
  class SchemaFile {
    +dialect: 2020-12
  }
  Spec "1" *-- "1" FrontMatter : starts with
  FrontMatter --> Status : status
  FrontMatter --> Kind : kind
  Spec "1" *-- "0..1" SchemaFile : protocol only
  Spec "*" --> "*" Spec : replaces
  Spec "*" --> "*" Spec : replaced_by
  Spec "*" --> "*" Spec : protocols, structures
```

## Elements

| Element | Path | Meaning |
| --- | --- | --- |
| `Spec` | src/spezi/project.py | One spec file with its number, its full rule ID and its Markdown body. |
| `FrontMatter` | specs/.templates/TEMPLATE.md | The YAML block at the start of a spec file (spec 000009). |
| `Status` | specs/conventions/specs/format/000010_status.md | The approval state of a spec (spec 000010). |
| `Kind` | specs/conventions/specs/layout/000004_tree.md | The type of a spec, given by its kind folder (spec 000004). |
| `SchemaFile` | specs/.templates/TEMPLATE-protocol.md | The JSON Schema beside a protocol spec of a JSON format (spec 000028). |

Reason: The diagram shows in one view how the parts of a spec and the links between specs fit
together.

Test: Review. `spezi check` checks the keys (spec 000009).
