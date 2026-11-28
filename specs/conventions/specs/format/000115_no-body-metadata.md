---
id: "000115"
title: The body holds no metadata
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/
scope:
  - specs/
---

# The body holds no metadata

The Markdown body of a spec must not hold metadata. Metadata goes into the front matter
(spec 000009).

Reason: A tool reads the metadata only from the front matter.

Test: Review.
