---
name: spezi-structure
description: Write or update a structure spec in specs/structures/, a UML diagram in Mermaid (class, state, sequence, entity, component) with an element table. Use to document a data model, a life cycle, a message sequence or a component layout.
---

# Write a structure spec

The rules are (spec 000033) to (spec 000039) in `specs/conventions/specs/structures/`.

## Steps

1. Choose one structure. One spec shows one diagram (spec 000033). Split a structure with more than
   25 elements (spec 000037), for example one spec for each module.
2. Choose the diagram type and set `diagram` (spec 000034):

   | `diagram` | First line | Use for |
   | --- | --- | --- |
   | `class` | `classDiagram` | Classes, models, their relations. |
   | `state` | `stateDiagram-v2` | The states of one life cycle. |
   | `sequence` | `sequenceDiagram` | Messages between parts, in time order. |
   | `entity` | `erDiagram` | Tables, columns, foreign keys. |
   | `component` | `flowchart` | Services, modules and their connections. |

3. Run `spezi new structure <area>/<topic> <name> "<title>" --scope <path>`. It copies
   `specs/.templates/TEMPLATE-structure.md` and gives the number (spec 000008).
4. Read the code. Draw what the code does now, not a plan (spec 000038). For a plan, set
   `status: draft` and `implementation: null`.
5. Write the diagram:
   - Use the names of the code, so that a search finds them.
   - Do not use `style`, `classDef`, `linkStyle`, `click`, `cssClass` or `:::` (spec 000034).
   - Give each relation a short label.
6. Fill `## Elements`: one row for each element, with the name of the diagram, the path of the
   code (or `-` for an external part) and one sentence of meaning (spec 000035, 000036).
7. Write the rule text: which part of the code must agree with the diagram. Use `must`.
8. Put the element paths, or their folders, in `implementation` (spec 000036).
9. Add the number to `structures` of each rule that depends on the structure (spec 000039).
10. Run `spezi install`. Fix each error.
11. Look at the diagram in the GitHub preview of the pull request. GitHub draws Mermaid blocks.

## Keep a structure spec current

A pull request that adds, removes or renames an element or a relation must change the diagram
too (spec 000038). Search `specs/structures/` for the changed path:

```sh
grep -rl "<changed path>" specs/structures
```
