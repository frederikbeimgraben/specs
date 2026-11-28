---
id: "000112"
title: The front matter is valid YAML
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_check.py:test_check_finds_front_matter_that_is_no_yaml
implementation:
  - src/spezi/check.py
  - src/spezi/project.py
scope:
  - specs/
---

# The front matter is valid YAML

The front matter block (spec 000111) must be valid YAML.

Reason: One YAML parser then reads every spec.

Test: `spezi check` reads the block with a YAML parser.
