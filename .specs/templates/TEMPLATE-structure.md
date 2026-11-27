---
id: "NNNNNN"
title: Short title of the structure
kind: structure
status: draft
owner: your-github-login
updated: YYYY-MM-DD
diagram: class
implementation: null
scope:
  - src/example
---

# Short title of the structure

The rule in one to three sentences: which part of the code must agree with the diagram. Use
`must` and `must not`.

## Diagram

```mermaid
classDiagram
  class Order {
    +id: UUID
    +status: OrderStatus
  }
  class Line {
    +quantity: int
  }
  Order "1" *-- "1..*" Line : holds
```

## Elements

| Element | Path | Meaning |
| --- | --- | --- |
| `Order` | - | One order of one customer. |
| `Line` | - | One product and its quantity in an order. |

Reason: The cause of the rule.

Test: The test or the review that finds a difference between the code and the diagram.
