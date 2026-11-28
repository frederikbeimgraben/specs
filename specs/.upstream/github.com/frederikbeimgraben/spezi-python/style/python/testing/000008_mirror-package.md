---
id: "000008"
title: tests/ mirrors the folders of a package with subpackages
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# tests/ mirrors the folders of a package with subpackages

When the package below `src/` has a subpackage, the folders below `tests/` must have the same
structure as the folders of the package. Else each test file must be directly in `tests/`.

Reason: In a large package, the folder of a module tells the folder of its tests. A small package
stays flat.

Test: A review compares the folders below `tests/` with the folders of the package.
