"""Check the specs of a project and write its index.

The check covers the spec conventions: the file name, the place in the tree, the front matter,
the headings, the labels, `must` in the rule text, the paths, `replaces`, unique numbers, the
index and every `§` reference in the code. For a protocol spec it also checks the sections, the
schema file and the examples. For a structure spec it checks the Mermaid block and the element
table. For a decision spec it checks the sections.
"""

from __future__ import annotations

import json
import re
import subprocess
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import jsonschema
from jsonschema.protocols import Validator

from specs_kit.project import (
    IN_FORCE,
    KINDS,
    KINDS_BY_PREFIX,
    LONG_LOCAL,
    NUMBER,
    PREFIXES,
    REPO,
    SHORT,
    STATUSES,
    Project,
    Spec,
)

KEYS = (
    "id",
    "title",
    "kind",
    "status",
    "owner",
    "updated",
    "replaced_by",
    "replaces",
    "version",
    "media_type",
    "diagram",
    "tests",
    "protocols",
    "structures",
    "implementation",
    "scope",
)
REQUIRED = frozenset({"id", "title", "kind", "status", "owner", "updated", "scope"})
VERSION = re.compile(r"^[1-9][0-9]*$")
MEDIA_TYPE = re.compile(r"^[a-z]+/[a-z0-9.+-]+$")
TEST_ENTRY = re.compile(r"^[^:\s]+:[A-Za-z_][A-Za-z0-9_.]*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LABEL = re.compile(r"^(Reason|Test):", re.MULTILINE)
MUST = re.compile(r"\bmust\b")
CODE_REF = re.compile(rf"§((?:{REPO}:)?{NUMBER})(?![0-9])")
CODE_LONG_REF = re.compile(rf"§((?:{REPO}:)?{LONG_LOCAL})")
SPEC_SECTION_REF = re.compile(rf"§ ?(?:(?:{REPO}:)?(?:{PREFIXES})/[a-z0-9/-]+/)?{NUMBER}\b")
FOREIGN_REF = re.compile(rf"(?<![\w/.-])({REPO}):({NUMBER})\b")
FOREIGN_LONG_REF = re.compile(rf"(?<![\w/.-])({REPO}):({LONG_LOCAL})\b")
INLINE_CODE = re.compile(r"`[^`\n]*`")

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

type Errors = tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Context:
    """What every check of one spec can read.

    Attributes:
        project: The project.
        local: The specs of the project by number.
        foreign: The status of each rule of the copies by short form. A rule that a spec in
            force replaces has the status `replaced` (§000049).
    """

    project: Project
    local: Mapping[str, Spec]
    foreign: Mapping[str, str]


def where(project: Project, spec: Spec) -> str:
    """Return the path of a spec from the root of the project.

    Args:
        project: The project.
        spec: The spec.

    Returns:
        The path as text.
    """
    return spec.path.relative_to(project.root).as_posix()


def _paths(ctx: Context, spec: Spec, key: str) -> Errors:
    """Return an error for each path of a list key that does not exist.

    Args:
        ctx: The context of the check.
        spec: The spec.
        key: The key of the front matter.

    Returns:
        The errors.
    """
    return tuple(
        f"{where(ctx.project, spec)}: {key} path {p!r} does not exist (000009)"
        for p in spec.entries(key) or ()
        if not (ctx.project.root / p).exists()
    )


def _check_implementation(ctx: Context, spec: Spec) -> Errors:
    """Check `implementation` against the status.

    Args:
        ctx: The context of the check.
        spec: The spec.

    Returns:
        The errors.
    """
    rel = where(ctx.project, spec)
    value = spec.meta.get("implementation")
    match spec.status in IN_FORCE, value:
        case True, "null":
            return ()
        case True, tuple() if value:
            return _paths(ctx, spec, "implementation")
        case True, _:
            return (f"{rel}: implementation must be a list of paths or null (000009)",)
        case False, None:
            return ()
        case False, _:
            return (f"{rel}: implementation goes with status draft or approved only (000009)",)


def _check_meta(ctx: Context, spec: Spec) -> Errors:
    """Check the front matter of one spec.

    Args:
        ctx: The context of the check.
        spec: The spec.

    Returns:
        The errors.
    """
    rel = where(ctx.project, spec)
    order = tuple(k for k in KEYS if k in spec.keys)
    raw_id = spec.path.read_text(encoding="utf-8").split("\n", 2)[1]
    kind = KINDS_BY_PREFIX.get(spec.prefix)
    tests = spec.entries("tests") or ()
    scope = spec.entries("scope")
    return (
        *(
            (f"{rel}: front matter keys or their order break 000009: {list(spec.keys)}",)
            if spec.keys != order or set(spec.keys) - set(KEYS) or REQUIRED - set(spec.keys)
            else ()
        ),
        *(
            ()
            if raw_id == f'id: "{spec.number}"'
            else (f"{rel}: id must be the quoted number of the file name (000009)",)
        ),
        *(
            ()
            if spec.meta.get("kind") == kind
            else (f"{rel}: kind {spec.meta.get('kind')!r} does not match the folder (000004)",)
        ),
        *(() if spec.status in STATUSES else (f"{rel}: status {spec.status!r} breaks 000010",)),
        *(
            ()
            if DATE.match(str(spec.meta.get("updated")))
            else (f"{rel}: updated must be YYYY-MM-DD (000009)",)
        ),
        *_check_kind_keys(ctx, spec),
        *_check_links(ctx, spec, "protocols", "P", "000032"),
        *_check_links(ctx, spec, "structures", "U", "000039"),
        *(
            f"{rel}: tests entry {entry!r} names no test file (000009)"
            for entry in tests
            if not TEST_ENTRY.match(entry) or not (ctx.project.root / entry.split(":")[0]).is_file()
        ),
        *_check_implementation(ctx, spec),
        *(
            _paths(ctx, spec, "scope")
            if scope
            else (f"{rel}: scope must be a list of paths (000009)",)
        ),
    )


def _check_kind_keys(ctx: Context, spec: Spec) -> Errors:
    """Check the keys that only one kind has: `version`, `media_type` and `diagram`.

    Args:
        ctx: The context of the check.
        spec: The spec.

    Returns:
        The errors.
    """
    rel, meta = where(ctx.project, spec), spec.meta
    pairs = (("version", "P"), ("media_type", "P"), ("diagram", "U"))
    return (
        *(
            f"{rel}: a {KINDS_BY_PREFIX[prefix]} spec must have {key} (000009)"
            for key, prefix in pairs
            if spec.prefix == prefix and key not in meta
        ),
        *(
            f"{rel}: {key} goes with kind {KINDS_BY_PREFIX[prefix]} only (000009)"
            for key, prefix in pairs
            if spec.prefix != prefix and key in meta
        ),
        *(
            (f"{rel}: version must be a whole number from 1 (000030)",)
            if "version" in meta and not VERSION.match(str(meta["version"]))
            else ()
        ),
        *(
            (f"{rel}: media_type {meta['media_type']!r} is no media type (000009)",)
            if "media_type" in meta and not MEDIA_TYPE.match(str(meta["media_type"]))
            else ()
        ),
        *(
            (f"{rel}: diagram must be one of {', '.join(DIAGRAMS)} (000034)",)
            if "diagram" in meta and meta["diagram"] not in DIAGRAMS
            else ()
        ),
    )


def _link_error(ctx: Context, rel: str, key: str, entry: str, prefix: str, rule: str) -> Errors:
    """Check one entry of `protocols` or `structures`.

    Args:
        ctx: The context of the check.
        rel: The path of the spec.
        key: The key of the front matter.
        entry: The short form of the linked spec.
        prefix: The kind letter that the linked spec must have.
        rule: The number of the rule for the message.

    Returns:
        The errors.
    """
    target = ctx.local.get(entry)
    match target:
        case None:
            return (f"{rel}: {key} entry {entry!r} names no spec; use the number ({rule})",)
        case Spec() if target.prefix != prefix:
            return (
                f"{rel}: {key} entry {entry!r} names no {KINDS_BY_PREFIX[prefix]} spec ({rule})",
            )
        case Spec() if target.status not in IN_FORCE:
            return (f"{rel}: {key} entry {entry!r} is not in force ({rule})",)
        case Spec():
            return ()


def _check_links(ctx: Context, spec: Spec, key: str, prefix: str, rule: str) -> Errors:
    """Check a list of linked specs, such as `protocols` or `structures`.

    Args:
        ctx: The context of the check.
        spec: The spec.
        key: The key of the front matter.
        prefix: The kind letter that each linked spec must have.
        rule: The number of the rule for the message.

    Returns:
        The errors.
    """
    rel = where(ctx.project, spec)
    value = spec.entries(key)
    if value is None:
        return ()
    kind_error = (
        (f"{rel}: {key} goes with an F or NF spec only ({rule})",)
        if spec.prefix not in ("F", "NF")
        else ()
    )
    if not value:
        return (*kind_error, f"{rel}: {key} must be a list of spec numbers ({rule})")
    return (
        *kind_error,
        *(e for entry in value for e in _link_error(ctx, rel, key, entry, prefix, rule)),
        *(
            (f"{rel}: {key} lists a spec two times ({rule})",)
            if len(set(value)) != len(value)
            else ()
        ),
    )


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


def _is_json(media_type: object) -> bool:
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
    if not _is_json(spec.meta.get("media_type")):
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


def _check_plain(ctx: Context, spec: Spec) -> Errors:
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


def _check_body(ctx: Context, spec: Spec) -> Errors:
    """Check the headings, the labels, `must`, the `§` signs and the foreign references.

    Args:
        ctx: The context of the check.
        spec: The spec.

    Returns:
        The errors.
    """
    rel = where(ctx.project, spec)
    labels = LABEL.findall(spec.body)
    rule_text = LABEL.split(spec.body, maxsplit=1)[0]
    text = INLINE_CODE.sub("", spec.body)
    return (
        *SECTION_CHECKS.get(spec.prefix, _check_plain)(ctx, spec),
        *(
            ()
            if labels in ([], ["Reason"], ["Test"], ["Reason", "Test"])
            else (f"{rel}: labels must be Reason, then Test, once each (000015)",)
        ),
        *(
            (f"{rel}: the rule text has no must or must not (000021)",)
            if spec.status in IN_FORCE and not MUST.search(rule_text)
            else ()
        ),
        *(
            f"{rel}: a spec refers to a rule without § (000017): {ref}"
            for ref in SPEC_SECTION_REF.findall(text)
        ),
        *(
            f"{rel}: use the short form {repo}:{rule[-6:]} (000047)"
            for repo, rule in FOREIGN_LONG_REF.findall(text)
        ),
        *(
            e
            for repo, number in FOREIGN_REF.findall(text)
            for e in _foreign_error(rel, f"{repo}:{number}", ctx.foreign)
        ),
    )


def _foreign_error(rel: str, ref: str, foreign: Mapping[str, str]) -> Errors:
    """Check one reference to a rule of a different repository.

    Args:
        rel: Where the reference is.
        ref: The short form of the reference.
        foreign: The status of each rule of the copies.

    Returns:
        The errors.
    """
    match foreign.get(ref):
        case None:
            return (f"{rel}: {ref} names no rule in .specs/upstream/ (000047)",)
        case "replaced":
            return (f"{rel}: {ref} names a rule that a project spec replaces (000049)",)
        case status if status in IN_FORCE:
            return ()
        case _:
            return (f"{rel}: {ref} names a rule that is not in force (000049)",)


def _replaces_entry(ctx: Context, spec: Spec, entry: str, foreign: Mapping[str, str]) -> Errors:
    """Check one entry of `replaces`.

    Args:
        ctx: The context of the check.
        spec: The spec that replaces.
        entry: The short form of the replaced rule.
        foreign: The status of each rule of the copies, before `replaces`.

    Returns:
        The errors.
    """
    rel = where(ctx.project, spec)
    target = ctx.local.get(entry)
    match SHORT.match(entry):
        case None:
            return (f"{rel}: replaces entry {entry!r} is not a short form (000047)",)
        case _ if entry == spec.number:
            return (f"{rel}: a spec must not replace itself (000009)",)
        case m if m.group(1):
            return (
                ()
                if entry in foreign
                else (
                    f"{rel}: replaces entry {entry!r} names no rule in .specs/upstream/ (000047)",
                )
            )
        case _ if target is None:
            return (f"{rel}: replaces entry {entry!r} names no spec (000009)",)
        case _ if target.status != "replaced":
            return (f"{rel}: {entry} must have status replaced (000010)",)
        case _ if spec.number not in (target.entries("replaced_by") or ()):
            return (f"{where(ctx.project, target)}: replaced_by must name {spec.number} (000010)",)
        case _:
            return ()


def _replaced_by_entry(ctx: Context, spec: Spec, entry: str) -> Errors:
    """Check one entry of `replaced_by`.

    Args:
        ctx: The context of the check.
        spec: The replaced spec.
        entry: The number of the spec that replaces it.

    Returns:
        The errors.
    """
    rel = where(ctx.project, spec)
    target = ctx.local.get(entry)
    match target:
        case None:
            return (
                f"{rel}: replaced_by entry {entry!r} names no spec of this repository (000009)",
            )
        case Spec() if (
            spec.number not in (target.entries("replaces") or ()) or target.status not in IN_FORCE
        ):
            return (f"{rel}: {entry} is not in force or does not name it in replaces (000010)",)
        case Spec():
            return ()


def _check_replaces(ctx: Context, specs: tuple[Spec, ...], foreign: Mapping[str, str]) -> Errors:
    """Check `replaces`, `replaced_by` and the status `replaced` (§000009, §000010, §000049).

    Args:
        ctx: The context of the check.
        specs: The specs of the project.
        foreign: The status of each rule of the copies, before `replaces`.

    Returns:
        The errors.
    """
    replacing = tuple(s for s in specs if s.entries("replaces") is not None)
    named = frozenset(
        e for s in replacing if s.status in IN_FORCE for e in s.entries("replaces") or ()
    )
    return (
        *(
            f"{where(ctx.project, s)}: replaces must be a list of rule IDs (000009)"
            for s in replacing
            if not s.entries("replaces")
        ),
        *(
            f"{where(ctx.project, s)}: replaces goes with status draft or approved only (000009)"
            for s in replacing
            if s.status not in IN_FORCE
        ),
        *(
            e
            for s in replacing
            if s.status in IN_FORCE
            for entry in s.entries("replaces") or ()
            for e in _replaces_entry(ctx, s, entry, foreign)
        ),
        *(
            f"{where(ctx.project, s)}: replaced_by goes with status replaced only (000009)"
            for s in specs
            if s.status != "replaced" and s.entries("replaced_by") is not None
        ),
        *(
            f"{where(ctx.project, s)}: status replaced, but no spec in force names it in"
            " replaces (000010)"
            for s in specs
            if s.status == "replaced" and s.number not in named
        ),
        *(
            f"{where(ctx.project, s)}: replaced_by must be a list of rule numbers (000009)"
            for s in specs
            if s.status == "replaced" and s.entries("replaced_by") == ()
        ),
        *(
            e
            for s in specs
            if s.status == "replaced"
            for entry in s.entries("replaced_by") or ()
            for e in _replaced_by_entry(ctx, s, entry)
        ),
    )


def _upstream_errors(project: Project) -> Errors:
    """Check that `specs.toml` and the copies below `.specs/upstream/` agree (§000048).

    Args:
        project: The project.

    Returns:
        The errors.
    """
    upstream = project.config.upstream
    copies = project.copies()
    return (
        *(
            f".specs/upstream/{repo}: no repository of this name in specs.toml (000048)"
            for repo in sorted(copies - set(upstream))
        ),
        *(
            f"specs.toml: upstream {repo!r} is not <host>/<owner>/<repo> (000047)"
            for repo in sorted(upstream)
            if not re.fullmatch(REPO, repo)
        ),
        *(
            f"specs.toml: upstream {repo!r} must have ref (000048)"
            for repo, ref in sorted(upstream.items())
            if ref is None
        ),
        *(
            f"specs.toml: upstream {repo!r} has no copy in .specs/upstream/; run specs update"
            f" {repo} <ref> (000048)"
            for repo in sorted(upstream)
            if repo not in copies
        ),
    )


def _code_files(project: Project) -> Iterable[Path]:
    """Return the code files of `code_dirs`.

    Args:
        project: The project.

    Returns:
        The files.
    """
    return (
        path
        for folder in project.config.code_dirs
        for path in sorted((project.root / folder).rglob("*"))
        if path.is_file()
        and path.suffix in project.config.code_suffixes
        and "node_modules" not in path.parts
    )


def _code_ref_error(ctx: Context, rel: str, ref: str) -> Errors:
    """Check one `§` reference in the code.

    Args:
        ctx: The context of the check.
        rel: The path of the code file.
        ref: The short form after `§`.

    Returns:
        The errors.
    """
    return (
        _foreign_error(rel, ref, ctx.foreign)
        if ":" in ref
        else (() if ref in ctx.local else (f"{rel}: §{ref} names no spec (000017)",))
    )


def _code_refs(ctx: Context) -> Errors:
    """Check the `§` references in the code (§000017, §000047).

    Args:
        ctx: The context of the check.

    Returns:
        The errors.
    """
    texts = tuple(
        (p.relative_to(ctx.project.root).as_posix(), p.read_text(encoding="utf-8", errors="ignore"))
        for p in _code_files(ctx.project)
    )
    return (
        *(
            f"{rel}: §{ref} must use the short form (000017)"
            for rel, text in texts
            for ref in CODE_LONG_REF.findall(text)
        ),
        *(
            e
            for rel, text in texts
            for ref in CODE_REF.findall(text)
            for e in _code_ref_error(ctx, rel, ref)
        ),
    )


def _git(project: Project, *args: str) -> str | None:
    """Run git in the project and return its output, or None when it fails.

    Args:
        project: The project.
        *args: The arguments of git.

    Returns:
        The output, or None.
    """
    try:
        return subprocess.run(
            ["git", *args], cwd=project.root, capture_output=True, text=True, check=True
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return None


def git_numbers(project: Project, ref: str) -> Mapping[str, str] | None:
    """Return number to spec path at a git ref.

    Args:
        project: The project.
        ref: The git ref.

    Returns:
        The paths by number, or None when git cannot read the ref.
    """
    out = _git(project, "ls-tree", "-r", "--name-only", ref, "--", "specs")
    return (
        None
        if out is None
        else {
            Path(line).name[:6]: line
            for line in out.splitlines()
            if re.match(r"^[0-9]{6}_", Path(line).name)
        }
    )


def _base_errors(project: Project, specs: tuple[Spec, ...]) -> Errors:
    """Return the numbers that the base branch gave to a different spec (§000013).

    A number collides when the base branch added it after the branch left the base branch, and
    the working tree has it at a different path. A checkout without the ref checks nothing.

    Args:
        project: The project.
        specs: The specs of the project.

    Returns:
        The errors.
    """
    base_ref = project.config.base_ref
    fork_ref = (_git(project, "merge-base", "HEAD", base_ref) or "").strip()
    base = git_numbers(project, base_ref) if fork_ref else None
    fork = git_numbers(project, fork_ref) if fork_ref else None
    if base is None or fork is None:
        return ()
    return tuple(
        f"{where(project, s)}: number {s.number} is {base[s.number]} on {base_ref}; give the"
        " spec a new number (000013)"
        for s in sorted(specs, key=lambda s: s.number)
        if s.number in base and s.number not in fork and base[s.number] != where(project, s)
    )


def _number_errors(project: Project, specs: tuple[Spec, ...]) -> Errors:
    """Return an error for each number that two specs use (§000013).

    Args:
        project: The project.
        specs: The specs of the project.

    Returns:
        The errors.
    """
    first = {s.number: s for s in reversed(specs)}
    return tuple(
        f"{where(project, s)}: number used by {where(project, first[s.number])} (000013)"
        for s in specs
        if first[s.number] is not s
    )


def _schema_errors(project: Project, specs: tuple[Spec, ...]) -> Errors:
    """Return an error for each schema file that no protocol spec owns (§000028).

    Args:
        project: The project.
        specs: The specs of the project.

    Returns:
        The errors.
    """
    owned = frozenset(schema_path(s.path) for s in specs if s.prefix == "P")
    folder = project.specs_dir / "protocols"
    return tuple(
        f"{p.relative_to(project.root).as_posix()}: no protocol spec owns this schema file (000028)"
        for p in (sorted(folder.rglob("*.json")) if folder.is_dir() else ())
        if p not in owned
    )


def foreign_status(project: Project, specs: tuple[Spec, ...]) -> Mapping[str, str]:
    """Return the status of each rule of the copies by short form (§000049).

    A rule that a spec of the project in force names in `replaces` gets the status `replaced`.

    Args:
        project: The project.
        specs: The specs of the project.

    Returns:
        The status by short form.
    """
    replaced = frozenset(
        e for s in specs if s.status in IN_FORCE for e in s.entries("replaces") or () if ":" in e
    )
    return {
        s.short: "replaced" if s.short in replaced else s.status for s in project.load_upstream()
    }


def _topics(area: Path) -> str:
    """Return the topic folders of one area folder, sorted and joined.

    Args:
        area: The area folder.

    Returns:
        The names of the topics.
    """
    return ", ".join(sorted(t.name for t in area.iterdir() if t.is_dir()))


def _tree_lines(base: Path, folder: str, indent: str) -> tuple[str, ...]:
    """Return the tree lines of one kind folder.

    Args:
        base: The kind folder.
        folder: The name of the kind folder below `specs/`.
        indent: The indent of the area lines.

    Returns:
        The lines.
    """
    areas = sorted(p for p in base.iterdir() if p.is_dir())
    width = max(len(a.name) for a in areas) + 2
    return (
        f"{indent[:-2]}{folder.split('/')[-1]}/",
        *(f"{indent}{(a.name + '/').ljust(width)} {_topics(a)}".rstrip() for a in areas),
    )


def tree(project: Project) -> str:
    """Return the tree block of the index from the folders.

    Args:
        project: The project.

    Returns:
        The tree text.
    """
    groups = tuple(
        (folder, project.specs_dir / folder, "      " if "/" in folder else "    ")
        for folder in KINDS
        if (project.specs_dir / folder).is_dir()
        and any(p.is_dir() for p in (project.specs_dir / folder).iterdir())
    )
    first_requirement = next((f for f, _, _ in groups if f.startswith("requirements/")), None)
    copies = sorted(project.copies())
    return (
        "\n".join(
            (
                "specs/",
                *(
                    line
                    for folder, base, indent in groups
                    for line in (
                        *(("  requirements/",) if folder == first_requirement else ()),
                        *_tree_lines(base, folder, indent),
                    )
                ),
                *((".specs/upstream/", *(f"  {repo}/" for repo in copies)) if copies else ()),
            )
        )
        + "\n"
    )


def _row(spec: Spec) -> str:
    """Return the index row of one spec, with a link from the root of the repository.

    Args:
        spec: The spec.

    Returns:
        The row.
    """
    folder = f".specs/upstream/{spec.repo}" if spec.repo else "specs"
    return f"| [{spec.long}](/{folder}/{spec.rel.as_posix()}) | {spec.title} | {spec.status} |"


def index(project: Project, specs: tuple[Spec, ...]) -> str:
    """Return the text of `.specs/index.md` and its copy `specs/README.md` (§000007).

    Args:
        project: The project.
        specs: The specs of the project.

    Returns:
        The whole text of the index.
    """
    foreign = foreign_status(project, specs)
    upstream = tuple(s for s in project.load_upstream() if foreign.get(s.short) in IN_FORCE)
    head = ("| ID | Title | Status |", "| --- | --- | --- |")
    return (
        "\n".join(
            (
                "# Specs",
                "",
                "The binding rules of this project. `specs/` holds only the rules of the",
                "project. The command `specs check --write` writes this file to",
                "`.specs/index.md` and to `specs/README.md`. Do not change these files by hand",
                "(000007).",
                "",
                "A new spec starts with",
                '`specs new <kind> <area>/<topic> <name> "<title>"` (000008).',
                "",
                "## Tree",
                "",
                "```",
                tree(project).rstrip("\n"),
                "```",
                "",
                "## Index",
                "",
                *head,
                *(_row(s) for s in sorted(specs, key=lambda s: s.full_id)),
                "",
                "## Upstream",
                "",
                "The rules of different repositories that apply to this project (000049).",
                "",
                *(
                    (*head, *(_row(s) for s in sorted(upstream, key=lambda s: s.long)))
                    if upstream
                    else ("No rules.",)
                ),
            )
        )
        + "\n"
    )


def _read(path: Path) -> str | None:
    """Return the text of a file, or None when it does not exist.

    Args:
        path: The file.

    Returns:
        The text, or None.
    """
    return path.read_text(encoding="utf-8") if path.is_file() else None


def run(project: Project, *, write: bool) -> tuple[int, Errors]:
    """Run every check. With `write`, write the index and its copy first.

    Args:
        project: The project.
        write: True to write `.specs/index.md` and `specs/README.md`.

    Returns:
        The count of specs and the errors.
    """
    specs, layout = project.load()
    foreign = foreign_status(project, specs)
    ctx = Context(project, {s.number: s for s in specs}, foreign)
    text = index(project, specs)
    if write:
        project.dot_dir.mkdir(parents=True, exist_ok=True)
        project.index_path.write_text(text, encoding="utf-8")
        project.readme_path.write_text(text, encoding="utf-8")
    raw = {s.short: s.status for s in project.load_upstream()}
    return len(specs), (
        *layout,
        *_upstream_errors(project),
        *_check_replaces(ctx, specs, raw),
        *_number_errors(project, specs),
        *(e for s in specs for e in (*_check_meta(ctx, s), *_check_body(ctx, s))),
        *_base_errors(project, specs),
        *_schema_errors(project, specs),
        *(
            ()
            if _read(project.index_path) == text
            else (".specs/index.md: the index is not current; run specs check --write (000007)",)
        ),
        *(
            ()
            if _read(project.readme_path) == text
            else (
                "specs/README.md: not an exact copy of the index; run specs check --write (000007)",
            )
        ),
        *_code_refs(ctx),
    )
