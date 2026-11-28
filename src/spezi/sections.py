"""Check the fixed sections of protocol, structure and decision specs, and the headings of the rest.

For a protocol spec the check covers the sections, the schema file and the examples. For a
structure spec it covers the Mermaid block and the element table. For a decision spec it covers
the sections.
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import cast

import jsonschema
from jsonschema.protocols import Validator

from spezi.context import Context, Errors, where
from spezi.project import Spec

PROTOCOL_SECTIONS = ("## Transport", "## Schema", "## Example", "## Compatibility")
SCHEMA_DIALECT = "https://json-schema.org/draft/2020-12/schema"
JSON_BLOCK = re.compile(r"^```json\n(.*?)^```", re.MULTILINE | re.DOTALL)
FENCE = re.compile(r"^```", re.MULTILINE)

STRUCTURE_SECTIONS = ("## Diagram", "## Elements")
DECISION_SECTIONS = ("## Context", "## Decision", "## Alternatives", "## Consequences")
DIAGRAMS: Mapping[str, tuple[str, ...]] = {
    "class": ("classDiagram",),
    "state": ("stateDiagram-v2", "stateDiagram"),
    "sequence": ("sequenceDiagram",),
    "entity": ("erDiagram",),
    "component": ("flowchart", "graph"),
}
MERMAID_STYLE = re.compile(
    r"^[ \t]*(?:(?:style|linkStyle)[ \t]+\S+[ \t]+\S|(?:classDef|click|cssClass)[ \t])|:::",
    re.MULTILINE,
)
MERMAID_BLOCK = re.compile(r"^```mermaid\n(.*?)^```", re.MULTILINE | re.DOTALL)
ELEMENTS_HEAD = "| Element | Path | Meaning |"
NAME = r"[A-Za-z_][A-Za-z0-9_-]*"
CLASS_LINK = r"(?:<\|--|\*--|o--|-->|<--|--\*|--o|--\|>|\.\.\|>|<\|\.\.|\.\.>|<\.\.|--|\.\.)"
FIND_ELEMENTS: Mapping[str, tuple[re.Pattern[str], ...]] = {
    "class": (
        re.compile(rf"^\s*class\s+({NAME})", re.MULTILINE),
        re.compile(
            rf'^\s*({NAME})\s*(?:"[^"]*"\s*)?{CLASS_LINK}\s*(?:"[^"]*"\s*)?({NAME})', re.MULTILINE
        ),
    ),
    "state": (
        re.compile(rf"^\s*state\s+(?:\"[^\"]*\"\s+as\s+)?({NAME})", re.MULTILINE),
        re.compile(rf"^\s*(\[\*\]|{NAME})\s*-->\s*(\[\*\]|{NAME})", re.MULTILINE),
    ),
    "sequence": (
        re.compile(rf"^\s*(?:participant|actor)\s+({NAME})", re.MULTILINE),
        re.compile(
            rf"^\s*({NAME})\s*(?:-->>|->>|-->|->|--x|-x|--\)|-\))[+-]?\s*({NAME})\s*:", re.MULTILINE
        ),
    ),
    "entity": (
        re.compile(rf"^\s*({NAME})\s*\{{", re.MULTILINE),
        re.compile(
            rf"^\s*({NAME})\s*[|}}o][|o]?(?:--|\.\.)[|o][|{{o]?\s*({NAME})\s*:", re.MULTILINE
        ),
    ),
}


def _sections(body: str) -> Mapping[str, str]:
    """Return the text below each `##` heading of a body.

    Args:
        body: The Markdown body.

    Returns:
        The text by heading.
    """
    parts = re.split(r"^(## .+)$", body, flags=re.MULTILINE)
    return {parts[i]: parts[i + 1] for i in range(1, len(parts) - 1, 2)}


def _headings(spec: Spec) -> tuple[str, ...]:
    """Return the Markdown headings of a body, outside code blocks.

    Args:
        spec: The spec.

    Returns:
        The heading lines.
    """
    lines = spec.body.splitlines()
    fences = tuple(i for i, line in enumerate(lines) if line.startswith("```"))
    return tuple(
        line
        for i, line in enumerate(lines)
        if line.startswith("#") and sum(1 for f in fences if f < i) % 2 == 0
    )


def schema_path(spec_path: Path) -> Path:
    """Return the path of the schema file beside a protocol spec (§000028).

    Args:
        spec_path: The path of the protocol spec.

    Returns:
        The path of the schema file.
    """
    return spec_path.with_name(spec_path.name[: -len(".md")] + ".schema.json")


def is_json(media_type: object) -> bool:
    """Return True for `application/json` and every `+json` media type.

    Args:
        media_type: The value of `media_type`.

    Returns:
        True for a JSON format.
    """
    return media_type == "application/json" or str(media_type).endswith("+json")


def _check_plain_protocol(rel: str, schema: Path, sections: Mapping[str, str]) -> Errors:
    """Check a protocol spec of a format that is not JSON.

    Args:
        rel: The path of the spec.
        schema: The path that a schema file would have.
        sections: The sections of the body.

    Returns:
        The errors.
    """
    return (
        *(
            (f"{rel}: a format that is not JSON has no schema file (000028)",)
            if schema.exists()
            else ()
        ),
        *(
            ()
            if re.search(r"^\|", sections.get("## Schema", ""), re.MULTILINE)
            else (f"{rel}: ## Schema of a format that is not JSON must hold a table (000028)",)
        ),
    )


def _read_schema(rel: str, schema: Path) -> dict[str, object] | str:
    """Read the schema file of a protocol spec.

    Args:
        rel: The path of the spec.
        schema: The path of the schema file.

    Returns:
        The schema, or the error.
    """
    if not schema.is_file():
        return f"{rel}: the schema file {schema.name} is missing (000028)"
    try:
        data: object = json.loads(schema.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return f"{rel}: {schema.name} is no JSON: {error} (000028)"
    return (
        cast("dict[str, object]", data)
        if isinstance(data, dict)
        and cast("dict[str, object]", data).get("$schema") == SCHEMA_DIALECT
        else f"{rel}: {schema.name} must set $schema to {SCHEMA_DIALECT} (000028)"
    )


def _check_protocol(ctx: Context, spec: Spec) -> Errors:
    """Check the sections, the schema file and the examples of a protocol spec.

    Args:
        ctx: The context of the check.
        spec: The spec.

    Returns:
        The errors.
    """
    rel = where(ctx.project, spec)
    if _headings(spec) != (f"# {spec.title}", *PROTOCOL_SECTIONS):
        return (
            f"{rel}: the body must have the # title, then {', '.join(PROTOCOL_SECTIONS)} (000027)",
        )
    sections = _sections(spec.body)
    example = sections.get("## Example", "")
    if len(FENCE.findall(example)) < 2:
        return (f"{rel}: ## Example must hold at least one code block (000029)",)
    schema = schema_path(spec.path)
    if not is_json(spec.meta.get("media_type")):
        return _check_plain_protocol(rel, schema, sections)
    data = _read_schema(rel, schema)
    return (data,) if isinstance(data, str) else _check_examples(rel, data, example)


def _example_errors(rel: str, validator: Validator, number: int, block: str) -> Errors:
    """Validate one `json` block of `## Example`.

    Args:
        rel: The path of the spec.
        validator: The validator of the schema.
        number: The position of the block, from 1.
        block: The text of the block.

    Returns:
        The errors.
    """
    try:
        instance = json.loads(block)
    except json.JSONDecodeError as error:
        return (f"{rel}: example {number} is no JSON: {error} (000029)",)
    return tuple(
        f"{rel}: example {number} at /{'/'.join(map(str, e.absolute_path))}: {e.message} (000029)"
        for e in validator.iter_errors(instance)
    )


def _check_examples(rel: str, schema: dict[str, object], example: str) -> Errors:
    """Validate the schema and each `json` block of `## Example` (§000028, §000029).

    Args:
        rel: The path of the spec.
        schema: The schema.
        example: The text of `## Example`.

    Returns:
        The errors.
    """
    validator_class = jsonschema.Draft202012Validator
    try:
        validator_class.check_schema(schema)
    except jsonschema.SchemaError as error:
        return (f"{rel}: the schema is no valid JSON Schema 2020-12: {error.message} (000028)",)
    validator = validator_class(schema, format_checker=validator_class.FORMAT_CHECKER)
    blocks = JSON_BLOCK.findall(example)
    return (
        tuple(
            e for n, b in enumerate(blocks, start=1) for e in _example_errors(rel, validator, n, b)
        )
        if blocks
        else (f"{rel}: ## Example has no json code block (000029)",)
    )


def diagram_elements(diagram: str, kind: str) -> frozenset[str]:
    """Return the element names that a Mermaid diagram of one kind declares or connects.

    Args:
        diagram: The text of the Mermaid block.
        kind: The diagram type.

    Returns:
        The element names.
    """
    text = re.sub(r"%%.*$", "", diagram, flags=re.MULTILINE)
    found = (
        name
        for pattern in FIND_ELEMENTS.get(kind, ())
        for match in cast("list[str | tuple[str, ...]]", pattern.findall(text))
        for name in (match if isinstance(match, tuple) else (match,))
    )
    return frozenset(found) - {"[*]"}


def _element_rows(section: str) -> tuple[tuple[str, str], ...] | None:
    """Return the name and the path of each row of the element table.

    Args:
        section: The text of `## Elements`.

    Returns:
        The rows, or None without a valid table.
    """
    lines = tuple(ln.strip() for ln in section.splitlines() if ln.strip().startswith("|"))
    if len(lines) < 3 or re.sub(r"\s+", " ", lines[0]) != ELEMENTS_HEAD:
        return None
    cells = tuple(tuple(c.strip().strip("`") for c in ln.strip("|").split("|")) for ln in lines[2:])
    return None if any(len(c) != 3 for c in cells) else tuple((c[0], c[1]) for c in cells)


def _check_rows(
    ctx: Context, rel: str, rows: tuple[tuple[str, str], ...], diagram: str, kind: str
) -> Errors:
    """Check the element table of a structure spec against its diagram.

    Args:
        ctx: The context of the check.
        rel: The path of the spec.
        rows: The rows of the element table.
        diagram: The text of the Mermaid block.
        kind: The diagram type.

    Returns:
        The errors.
    """
    limit = ctx.project.config.max_elements
    listed = frozenset(name for name, _ in rows)
    return (
        *(
            (f"{rel}: {len(rows)} elements; a diagram has at most {limit} (000037)",)
            if len(rows) > limit
            else ()
        ),
        *(
            f"{rel}: element {name!r} of the table is not in the diagram (000035)"
            for name, _ in rows
            if not re.search(rf"(?<![A-Za-z0-9_-]){re.escape(name)}(?![A-Za-z0-9_-])", diagram)
        ),
        *(
            f"{rel}: path {path!r} of element {name!r} does not exist (000036)"
            for name, path in rows
            if path != "-" and not (ctx.project.root / path).exists()
        ),
        *(
            f"{rel}: element {name!r} of the diagram has no row in ## Elements (000035)"
            for name in sorted(diagram_elements(diagram, kind) - listed)
        ),
    )


def _check_structure(ctx: Context, spec: Spec) -> Errors:
    """Check the Mermaid block and the element table of a structure spec.

    Args:
        ctx: The context of the check.
        spec: The spec.

    Returns:
        The errors.
    """
    rel = where(ctx.project, spec)
    if _headings(spec) != (f"# {spec.title}", *STRUCTURE_SECTIONS):
        return (
            f"{rel}: the body must have the # title, then {', '.join(STRUCTURE_SECTIONS)} (000033)",
        )
    sections = _sections(spec.body)
    blocks = MERMAID_BLOCK.findall(sections["## Diagram"])
    if len(blocks) != 1 or len(FENCE.findall(sections["## Diagram"])) != 2:
        return (f"{rel}: ## Diagram must hold exactly one mermaid code block (000034)",)
    diagram = cast("str", blocks[0])
    kind = str(spec.meta.get("diagram"))
    lines = tuple(
        ln.strip() for ln in diagram.splitlines() if ln.strip() and not ln.strip().startswith("%%")
    )
    first = lines[0].split()[0] if lines else ""
    rows = _element_rows(sections["## Elements"])
    head = (
        *(
            (f"{rel}: a {kind} diagram must start with {' or '.join(DIAGRAMS[kind])} (000034)",)
            if kind in DIAGRAMS and first not in DIAGRAMS[kind]
            else ()
        ),
        *(
            (f"{rel}: the diagram must not hold styles, colors or click actions (000034)",)
            if MERMAID_STYLE.search(diagram)
            else ()
        ),
    )
    return (
        (*head, f"{rel}: ## Elements must hold the table {ELEMENTS_HEAD} (000035)")
        if rows is None
        else (*head, *_check_rows(ctx, rel, rows, diagram, kind))
    )


def _check_decision(ctx: Context, spec: Spec) -> Errors:
    """Check the sections of a decision spec (§000042).

    Args:
        ctx: The context of the check.
        spec: The spec.

    Returns:
        The errors.
    """
    return (
        ()
        if _headings(spec) == (f"# {spec.title}", *DECISION_SECTIONS)
        else (
            f"{where(ctx.project, spec)}: the body must have the # title, then "
            f"{', '.join(DECISION_SECTIONS)} (000042)",
        )
    )


def check_plain(ctx: Context, spec: Spec) -> Errors:
    """Check the headings of a spec without fixed sections.

    Args:
        ctx: The context of the check.
        spec: The spec.

    Returns:
        The errors.
    """
    return (
        ()
        if _headings(spec) == (f"# {spec.title}",)
        else (
            f"{where(ctx.project, spec)}: the body must have one # heading equal to the title"
            " (000011)",
        )
    )


SECTION_CHECKS: Mapping[str, Callable[[Context, Spec], Errors]] = {
    "P": _check_protocol,
    "U": _check_structure,
    "D": _check_decision,
}
