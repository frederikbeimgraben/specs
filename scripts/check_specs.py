#!/usr/bin/env python3
"""Check the spec files in `specs/` and keep the index in `specs/README.md` current.

The script checks the spec conventions in `specs/conventions/specs/`: the file name, the place in
the tree, the front matter, the headings, the labels, `must` in the rule text, the paths,
`replaced_by`, unique numbers, the index and every `§` reference in the code. For a protocol
spec it also checks the sections, the schema file and the examples. For a structure spec it
checks the Mermaid block and the element table. For a decision spec it checks the sections.

The settings are in `specs/config.toml`. The script needs Python 3.11 or later. It needs the
package `jsonschema` only when a protocol spec has a JSON schema file.

Usage:
    python3 scripts/check_specs.py          check, exit 1 on a violation
    python3 scripts/check_specs.py --write  write the index of specs/README.md, then check
    python3 scripts/check_specs.py --fetch  replace the copies in specs/upstream/, then check
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPECS = ROOT / "specs"
UPSTREAM = SPECS / "upstream"
README = SPECS / "README.md"
CONFIG = SPECS / "config.toml"

KINDS = {
    "requirements/functional": ("F", "functional"),
    "requirements/non-functional": ("NF", "non-functional"),
    "protocols": ("P", "protocol"),
    "structures": ("U", "structure"),
    "style": ("S", "style"),
    "conventions": ("C", "convention"),
    "workflow": ("W", "workflow"),
    "agents": ("A", "agent"),
    "decisions": ("D", "decision"),
}
PREFIXES = "|".join(prefix for prefix, _ in KINDS.values())
KEYS = [
    "id",
    "title",
    "kind",
    "status",
    "owner",
    "updated",
    "replaced_by",
    "version",
    "media_type",
    "diagram",
    "tests",
    "protocols",
    "structures",
    "implementation",
    "scope",
]
REQUIRED = {"id", "title", "kind", "status", "owner", "updated", "scope"}
STATUSES = {"draft", "approved", "replaced", "removed"}
IN_FORCE = {"draft", "approved"}
FILE_NAME = re.compile(r"^[0-9]{6}_[a-z0-9]+(-[a-z0-9]+)*\.md$")
FOLDER = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FULL_ID = re.compile(rf"^({PREFIXES})(/[a-z0-9-]+)+/[0-9]{{6}}$")
VERSION = re.compile(r"^[1-9][0-9]*$")
MEDIA_TYPE = re.compile(r"^[a-z]+/[a-z0-9.+-]+$")
TEST_ENTRY = re.compile(r"^[^:\s]+:[A-Za-z_][A-Za-z0-9_.]*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LABEL = re.compile(r"^(Reason|Test):", re.MULTILINE)
MUST = re.compile(r"\bmust\b")
REPO = r"[a-z0-9.-]+\.[a-z]+/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+"
LOCAL_ID = rf"(?:{PREFIXES})/[a-z0-9/-]+/[0-9]{{6}}"
SECTION_REF = re.compile(rf"§((?:{REPO}:)?{LOCAL_ID})")
SPEC_SECTION_REF = re.compile(rf"§ ?(?:(?:{REPO}:)?(?:{PREFIXES})/[a-z0-9/-]+/)?[0-9]{{6}}\b")
FOREIGN_REF = re.compile(rf"(?<![\w/.-])({REPO}):({LOCAL_ID})\b")
INLINE_CODE = re.compile(r"`[^`\n]*`")
INDEX_START = "## Index\n"

PROTOCOL_SECTIONS = ["## Transport", "## Schema", "## Example", "## Compatibility"]
SCHEMA_DIALECT = "https://json-schema.org/draft/2020-12/schema"
JSON_BLOCK = re.compile(r"^```json\n(.*?)^```", re.MULTILINE | re.DOTALL)
FENCE = re.compile(r"^```", re.MULTILINE)

STRUCTURE_SECTIONS = ["## Diagram", "## Elements"]
DECISION_SECTIONS = ["## Context", "## Decision", "## Alternatives", "## Consequences"]
DIAGRAMS = {
    "class": ("classDiagram",),
    "state": ("stateDiagram-v2", "stateDiagram"),
    "sequence": ("sequenceDiagram",),
    "entity": ("erDiagram",),
    "component": ("flowchart", "graph"),
}
MERMAID_STYLE = re.compile(r"^[ \t]*(?:(?:style|linkStyle)[ \t]+\S+[ \t]+\S|(?:classDef|click|cssClass)[ \t])|:::", re.MULTILINE)
MERMAID_BLOCK = re.compile(r"^```mermaid\n(.*?)^```", re.MULTILINE | re.DOTALL)
ELEMENTS_HEAD = "| Element | Path | Meaning |"
NAME = r"[A-Za-z_][A-Za-z0-9_-]*"
FIND_ELEMENTS = {
    "class": [
        re.compile(rf"^\s*class\s+({NAME})", re.MULTILINE),
        re.compile(
            rf'^\s*({NAME})\s*(?:"[^"]*"\s*)?(?:<\|--|\*--|o--|-->|<--|--\*|--o|--\|>|\.\.\|>|<\|\.\.|\.\.>|<\.\.|--|\.\.)'
            rf'\s*(?:"[^"]*"\s*)?({NAME})',
            re.MULTILINE,
        ),
    ],
    "state": [
        re.compile(rf"^\s*state\s+(?:\"[^\"]*\"\s+as\s+)?({NAME})", re.MULTILINE),
        re.compile(rf"^\s*(\[\*\]|{NAME})\s*-->\s*(\[\*\]|{NAME})", re.MULTILINE),
    ],
    "sequence": [
        re.compile(rf"^\s*(?:participant|actor)\s+({NAME})", re.MULTILINE),
        re.compile(rf"^\s*({NAME})\s*(?:-->>|->>|-->|->|--x|-x|--\)|-\))[+-]?\s*({NAME})\s*:", re.MULTILINE),
    ],
    "entity": [
        re.compile(rf"^\s*({NAME})\s*\{{", re.MULTILINE),
        re.compile(rf"^\s*({NAME})\s*[|}}o][|o]?(?:--|\.\.)[|o][|{{o]?\s*({NAME})\s*:", re.MULTILINE),
    ],
}


@dataclass(frozen=True)
class Spec:
    """One parsed spec file."""

    path: Path
    full_id: str
    meta: dict[str, str | list[str]]
    keys: list[str]
    body: str

    @property
    def rel(self) -> Path:
        """Return the path below `specs/`."""
        return self.path.relative_to(SPECS)

    @property
    def prefix(self) -> str:
        """Return the kind letter of the rule ID."""
        return self.full_id.split("/", 1)[0]


def _config() -> dict[str, object]:
    """Return the settings of `specs/config.toml`, with defaults for a missing key."""
    data: dict[str, object] = {}
    if CONFIG.is_file():
        data = tomllib.loads(CONFIG.read_text(encoding="utf-8"))
    return {
        "base_ref": data.get("base_ref", "origin/main"),
        "code_dirs": data.get("code_dirs", []),
        "code_suffixes": set(data.get("code_suffixes", [".py", ".ts", ".js", ".go", ".rs", ".java"])),
        "max_elements": int(data.get("max_elements", 25)),
        "upstream": data.get("upstream", {}),
    }


def _parse_front_matter(text: str) -> tuple[dict[str, str | list[str]], list[str], str] | None:
    """Return the keys, their order and the body, or None without front matter."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    meta: dict[str, str | list[str]] = {}
    keys: list[str] = []
    current: str | None = None
    for line in text[4:end].splitlines():
        if line.startswith("  - ") and current is not None:
            value = meta.setdefault(current, [])
            if isinstance(value, list):
                value.append(line[4:].strip().strip('"'))
            continue
        key, _, value = line.partition(":")
        current = key.strip()
        keys.append(current)
        meta[current] = value.strip().strip('"') if value.strip() else []
    return meta, keys, text[end + 5 :]


def _kind_of(rel: Path) -> tuple[str, str, Path] | None:
    """Return the ID prefix, the kind and the path below the kind folder."""
    for folder, (prefix, kind) in KINDS.items():
        base = Path(folder)
        if rel.parts[: len(base.parts)] == base.parts:
            return prefix, kind, Path(*rel.parts[len(base.parts) :])
    return None


def load() -> tuple[list[Spec], list[str]]:
    """Parse every spec file and return the specs and the errors of the file layout."""
    specs: list[Spec] = []
    errors: list[str] = []
    for path in sorted(SPECS.rglob("*.md")):
        rel = path.relative_to(SPECS)
        if rel.parent == Path(".") or rel.parts[0] == "upstream":
            continue
        kind = _kind_of(rel)
        if kind is None:
            errors.append(f"{rel}: not below a kind folder (000004)")
            continue
        prefix, _, below = kind
        if len(below.parts) != 3:
            errors.append(f"{rel}: must be <area>/<topic>/<file> below the kind folder (000004)")
            continue
        if not FILE_NAME.match(path.name):
            errors.append(f"{rel}: file name breaks 000016")
        for folder in below.parts[:2]:
            if not FOLDER.match(folder):
                errors.append(f"{rel}: folder {folder!r} breaks 000005")
        parsed = _parse_front_matter(path.read_text(encoding="utf-8"))
        if parsed is None:
            errors.append(f"{rel}: no front matter (000009)")
            continue
        meta, keys, body = parsed
        full_id = f"{prefix}/{below.parts[0]}/{below.parts[1]}/{path.name[:6]}"
        specs.append(Spec(path, full_id, meta, keys, body))
    return specs, errors


def _paths(spec: Spec, key: str) -> list[str]:
    """Return an error for each path of a list key that does not exist."""
    value = spec.meta.get(key)
    if not isinstance(value, list):
        return []
    return [f"{spec.rel}: {key} path {p!r} does not exist (000009)" for p in value if not (ROOT / p).exists()]


def _check_meta(spec: Spec, ids: dict[str, Spec]) -> list[str]:
    """Check the front matter of one spec."""
    rel, meta = spec.rel, spec.meta
    errors: list[str] = []
    order = [k for k in KEYS if k in spec.keys]
    if spec.keys != order or set(spec.keys) - set(KEYS) or REQUIRED - set(spec.keys):
        errors.append(f"{rel}: front matter keys or their order break 000009: {spec.keys}")
    raw_id = spec.path.read_text(encoding="utf-8").split("\n", 2)[1]
    if raw_id != f'id: "{spec.path.name[:6]}"':
        errors.append(f"{rel}: id must be the quoted number of the file name (000009)")
    kind = _kind_of(rel)
    if kind is not None and meta.get("kind") != kind[1]:
        errors.append(f"{rel}: kind {meta.get('kind')!r} does not match the folder (000004)")
    status = meta.get("status")
    if status not in STATUSES:
        errors.append(f"{rel}: status {status!r} breaks 000010")
    if not DATE.match(str(meta.get("updated"))):
        errors.append(f"{rel}: updated must be YYYY-MM-DD (000009)")
    replaced_by = meta.get("replaced_by")
    if (status == "replaced") != (replaced_by is not None):
        errors.append(f"{rel}: replaced_by goes with status replaced only (000009)")
    if isinstance(replaced_by, str):
        target = ids.get(replaced_by)
        if not FULL_ID.match(replaced_by) or target is None:
            errors.append(f"{rel}: replaced_by {replaced_by!r} is no full ID of a spec (000009)")
        elif target.meta.get("status") not in IN_FORCE:
            errors.append(f"{rel}: replaced_by points to a rule that is not in force (000009)")
    errors += _check_kind_keys(spec)
    errors += _check_links(spec, ids, "protocols", "P", "000032")
    errors += _check_links(spec, ids, "structures", "U", "000039")
    tests = meta.get("tests", [])
    for entry in tests if isinstance(tests, list) else [tests]:
        if not TEST_ENTRY.match(entry) or not (ROOT / entry.split(":")[0]).is_file():
            errors.append(f"{rel}: tests entry {entry!r} names no test file (000009)")
    implementation = meta.get("implementation")
    if status in IN_FORCE:
        if implementation != "null" and (not isinstance(implementation, list) or not implementation):
            errors.append(f"{rel}: implementation must be a list of paths or null (000009)")
        errors += _paths(spec, "implementation")
    elif implementation is not None:
        errors.append(f"{rel}: implementation goes with status draft or approved only (000009)")
    scope = meta.get("scope")
    if not isinstance(scope, list) or not scope:
        errors.append(f"{rel}: scope must be a list of paths (000009)")
    else:
        errors += _paths(spec, "scope")
    return errors


def _check_kind_keys(spec: Spec) -> list[str]:
    """Check the keys that only one kind has: `version`, `media_type` and `diagram`."""
    rel, meta = spec.rel, spec.meta
    errors: list[str] = []
    for key, prefix in (("version", "P"), ("media_type", "P"), ("diagram", "U")):
        if spec.prefix == prefix and key not in meta:
            errors.append(f"{rel}: a {KINDS_BY_PREFIX[prefix]} spec must have {key} (000009)")
        if spec.prefix != prefix and key in meta:
            errors.append(f"{rel}: {key} goes with kind {KINDS_BY_PREFIX[prefix]} only (000009)")
    if "version" in meta and not VERSION.match(str(meta["version"])):
        errors.append(f"{rel}: version must be a whole number from 1 (000030)")
    if "media_type" in meta and not MEDIA_TYPE.match(str(meta["media_type"])):
        errors.append(f"{rel}: media_type {meta['media_type']!r} is no media type (000009)")
    if "diagram" in meta and meta["diagram"] not in DIAGRAMS:
        errors.append(f"{rel}: diagram must be one of {', '.join(DIAGRAMS)} (000034)")
    return errors


KINDS_BY_PREFIX = {prefix: kind for prefix, kind in KINDS.values()}


def _check_links(spec: Spec, ids: dict[str, Spec], key: str, prefix: str, rule: str) -> list[str]:
    """Check a list of linked spec IDs, such as `protocols` or `structures`."""
    value = spec.meta.get(key)
    if value is None:
        return []
    errors: list[str] = []
    if spec.prefix not in ("F", "NF"):
        errors.append(f"{spec.rel}: {key} goes with an F or NF spec only ({rule})")
    if not isinstance(value, list) or not value:
        return [*errors, f"{spec.rel}: {key} must be a list of spec IDs ({rule})"]
    for entry in value:
        target = ids.get(entry)
        if not entry.startswith(f"{prefix}/") or target is None:
            errors.append(f"{spec.rel}: {key} entry {entry!r} names no {KINDS_BY_PREFIX[prefix]} spec ({rule})")
        elif target.meta.get("status") not in IN_FORCE:
            errors.append(f"{spec.rel}: {key} entry {entry!r} is not in force ({rule})")
    if len(set(value)) != len(value):
        errors.append(f"{spec.rel}: {key} lists an ID two times ({rule})")
    return errors


def _sections(body: str) -> dict[str, str]:
    """Return the text below each `##` heading of a body."""
    parts = re.split(r"^(## .+)$", body, flags=re.MULTILINE)
    return {parts[i]: parts[i + 1] for i in range(1, len(parts) - 1, 2)}


def _headings(spec: Spec) -> list[str]:
    """Return the Markdown headings of a body, outside code blocks."""
    out: list[str] = []
    fenced = False
    for line in spec.body.splitlines():
        if line.startswith("```"):
            fenced = not fenced
        elif not fenced and line.startswith("#"):
            out.append(line)
    return out


def schema_path(spec_path: Path) -> Path:
    """Return the path of the schema file beside a protocol spec (000028)."""
    return spec_path.with_name(spec_path.name[: -len(".md")] + ".schema.json")


def _is_json(media_type: object) -> bool:
    """Return True for `application/json` and every `+json` media type."""
    return media_type == "application/json" or str(media_type).endswith("+json")


def _check_protocol(spec: Spec) -> list[str]:
    """Check the sections, the schema file and the examples of a protocol spec."""
    rel = spec.rel
    if _headings(spec) != [f"# {spec.meta.get('title')}", *PROTOCOL_SECTIONS]:
        return [f"{rel}: the body must have the # title, then {', '.join(PROTOCOL_SECTIONS)} (000027)"]
    sections = _sections(spec.body)
    example = sections.get("## Example", "")
    if len(FENCE.findall(example)) < 2:
        return [f"{rel}: ## Example must hold at least one code block (000029)"]
    schema = schema_path(spec.path)
    if not _is_json(spec.meta.get("media_type")):
        errors = []
        if schema.exists():
            errors.append(f"{rel}: a format that is not JSON has no schema file (000028)")
        if not re.search(r"^\|", sections.get("## Schema", ""), re.MULTILINE):
            errors.append(f"{rel}: ## Schema of a format that is not JSON must hold a table (000028)")
        return errors
    if not schema.is_file():
        return [f"{rel}: the schema file {schema.name} is missing (000028)"]
    try:
        data = json.loads(schema.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [f"{rel}: {schema.name} is no JSON: {error} (000028)"]
    if not isinstance(data, dict) or data.get("$schema") != SCHEMA_DIALECT:
        return [f"{rel}: {schema.name} must set $schema to {SCHEMA_DIALECT} (000028)"]
    return _check_examples(spec, data, example)


def _check_examples(spec: Spec, schema: dict[str, object], example: str) -> list[str]:
    """Validate the schema and each `json` block of `## Example` (000028, 000029)."""
    try:
        import jsonschema  # noqa: PLC0415
    except ImportError:
        return [f"{spec.rel}: install the package jsonschema to check the schema (000029)"]
    validator_class = jsonschema.Draft202012Validator
    try:
        validator_class.check_schema(schema)
    except jsonschema.SchemaError as error:
        return [f"{spec.rel}: the schema is no valid JSON Schema 2020-12: {error.message} (000028)"]
    validator = validator_class(schema, format_checker=validator_class.FORMAT_CHECKER)
    blocks = JSON_BLOCK.findall(example)
    if not blocks:
        return [f"{spec.rel}: ## Example has no json code block (000029)"]
    errors: list[str] = []
    for number, block in enumerate(blocks, start=1):
        try:
            instance = json.loads(block)
        except json.JSONDecodeError as error:
            errors.append(f"{spec.rel}: example {number} is no JSON: {error} (000029)")
            continue
        errors += [
            f"{spec.rel}: example {number} at /{'/'.join(map(str, e.absolute_path))}: {e.message} (000029)"
            for e in validator.iter_errors(instance)
        ]
    return errors


def diagram_elements(diagram: str, kind: str) -> set[str]:
    """Return the element names that a Mermaid diagram of one kind declares or connects."""
    text = re.sub(r"%%.*$", "", diagram, flags=re.MULTILINE)
    names: set[str] = set()
    for pattern in FIND_ELEMENTS.get(kind, []):
        for match in pattern.findall(text):
            names.update(match if isinstance(match, tuple) else (match,))
    names.discard("[*]")
    return names


def _check_structure(spec: Spec, max_elements: int) -> list[str]:
    """Check the Mermaid block and the element table of a structure spec."""
    rel = spec.rel
    if _headings(spec) != [f"# {spec.meta.get('title')}", *STRUCTURE_SECTIONS]:
        return [f"{rel}: the body must have the # title, then {', '.join(STRUCTURE_SECTIONS)} (000033)"]
    sections = _sections(spec.body)
    blocks = MERMAID_BLOCK.findall(sections["## Diagram"])
    if len(blocks) != 1 or len(FENCE.findall(sections["## Diagram"])) != 2:
        return [f"{rel}: ## Diagram must hold exactly one mermaid code block (000034)"]
    diagram = blocks[0]
    kind = str(spec.meta.get("diagram"))
    lines = [ln.strip() for ln in diagram.splitlines() if ln.strip() and not ln.strip().startswith("%%")]
    first = lines[0].split()[0] if lines else ""
    errors: list[str] = []
    if kind in DIAGRAMS and first not in DIAGRAMS[kind]:
        errors.append(f"{rel}: a {kind} diagram must start with {' or '.join(DIAGRAMS[kind])} (000034)")
    if MERMAID_STYLE.search(diagram):
        errors.append(f"{rel}: the diagram must not hold styles, colors or click actions (000034)")
    rows = _element_rows(sections["## Elements"])
    if rows is None:
        return [*errors, f"{rel}: ## Elements must hold the table {ELEMENTS_HEAD} (000035)"]
    if len(rows) > max_elements:
        errors.append(f"{rel}: {len(rows)} elements; a diagram has at most {max_elements} (000037)")
    listed: set[str] = set()
    for name, path in rows:
        listed.add(name)
        if not re.search(rf"(?<![A-Za-z0-9_-]){re.escape(name)}(?![A-Za-z0-9_-])", diagram):
            errors.append(f"{rel}: element {name!r} of the table is not in the diagram (000035)")
        if path != "-" and not (ROOT / path).exists():
            errors.append(f"{rel}: path {path!r} of element {name!r} does not exist (000036)")
    errors += [
        f"{rel}: element {name!r} of the diagram has no row in ## Elements (000035)"
        for name in sorted(diagram_elements(diagram, kind) - listed)
    ]
    return errors


def _element_rows(section: str) -> list[tuple[str, str]] | None:
    """Return the name and the path of each row of the element table, or None without it."""
    lines = [ln.strip() for ln in section.splitlines() if ln.strip().startswith("|")]
    if len(lines) < 3 or re.sub(r"\s+", " ", lines[0]) != ELEMENTS_HEAD:
        return None
    rows: list[tuple[str, str]] = []
    for line in lines[2:]:
        cells = [c.strip().strip("`") for c in line.strip("|").split("|")]
        if len(cells) != 3:
            return None
        rows.append((cells[0], cells[1]))
    return rows


def _check_decision(spec: Spec) -> list[str]:
    """Check the sections of a decision spec (000042)."""
    if _headings(spec) != [f"# {spec.meta.get('title')}", *DECISION_SECTIONS]:
        return [f"{spec.rel}: the body must have the # title, then {', '.join(DECISION_SECTIONS)} (000042)"]
    return []


def _check_body(spec: Spec, max_elements: int) -> list[str]:
    """Check the headings, the labels, `must` and the `§` signs of one spec."""
    rel = spec.rel
    errors: list[str] = []
    if spec.prefix == "P":
        errors += _check_protocol(spec)
    elif spec.prefix == "U":
        errors += _check_structure(spec, max_elements)
    elif spec.prefix == "D":
        errors += _check_decision(spec)
    elif _headings(spec) != [f"# {spec.meta.get('title')}"]:
        errors.append(f"{rel}: the body must have one # heading equal to the title (000011)")
    labels = LABEL.findall(spec.body)
    if labels not in ([], ["Reason"], ["Test"], ["Reason", "Test"]):
        errors.append(f"{rel}: labels must be Reason, then Test, once each (000015)")
    rule_text = LABEL.split(spec.body, maxsplit=1)[0]
    if spec.meta.get("status") in IN_FORCE and not MUST.search(rule_text):
        errors.append(f"{rel}: the rule text has no must or must not (000021)")
    errors += [
        f"{rel}: a spec refers to a rule without § (000017): {ref}"
        for ref in SPEC_SECTION_REF.findall(INLINE_CODE.sub("", spec.body))
    ]
    return errors


def _index(specs: list[Spec]) -> str:
    """Return the index table of README.md."""
    rows = [
        f"| [{s.full_id}]({s.rel.as_posix()}) | {s.meta.get('title')} | {s.meta.get('status')} |"
        for s in sorted(specs, key=lambda s: s.full_id)
    ]
    return "\n".join(["| ID | Title | Status |", "| --- | --- | --- |", *rows]) + "\n"


def _tree() -> str:
    """Return the tree block of README.md from the folders."""
    lines = ["specs/"]
    groups: list[tuple[str, Path, str]] = []
    for folder in KINDS:
        base = SPECS / folder
        if base.is_dir() and any(p.is_dir() for p in base.iterdir()):
            groups.append((folder, base, "      " if "/" in folder else "    "))
    seen_requirements = False
    for folder, base, indent in groups:
        if folder.startswith("requirements/") and not seen_requirements:
            lines.append("  requirements/")
            seen_requirements = True
        lines.append(f"{indent[:-2]}{folder.split('/')[-1]}/")
        areas = sorted(p for p in base.iterdir() if p.is_dir())
        width = max(len(a.name) for a in areas) + 2
        for area in areas:
            topics = ", ".join(sorted(t.name for t in area.iterdir() if t.is_dir()))
            lines.append(f"{indent}{(area.name + '/').ljust(width)} {topics}".rstrip())
    if UPSTREAM.is_dir():
        repos = sorted(p.relative_to(UPSTREAM).as_posix() for p in UPSTREAM.glob("*/*/*") if p.is_dir())
        if repos:
            lines.append("  upstream/")
            lines += [f"    {repo}/" for repo in repos]
    return "\n".join(lines) + "\n"


def _readme(specs: list[Spec]) -> str:
    """Return README.md with a current tree and index."""
    text = README.read_text(encoding="utf-8")
    text = re.sub(r"```\nspecs/\n.*?```", lambda _: f"```\n{_tree()}```", text, flags=re.DOTALL)
    head = text[: text.index(INDEX_START) + len(INDEX_START)]
    return f"{head}\n{_index(specs)}"


def _upstream_ids(config: dict[str, object]) -> tuple[dict[str, str], list[str]]:
    """Return the status of each rule in the copies below `specs/upstream/` (000048, 000049).

    The keys are foreign references `<host>/<owner>/<repo>:<ID>`. An excluded rule has the
    status `excluded`.
    """
    upstream: dict[str, dict[str, object]] = config["upstream"]  # type: ignore[assignment]
    ids: dict[str, str] = {}
    errors: list[str] = []
    copies = {p.relative_to(UPSTREAM).as_posix() for p in UPSTREAM.glob("*/*/*") if p.is_dir()} if UPSTREAM.is_dir() else set()
    for repo in sorted(copies - set(upstream)):
        errors.append(f"specs/upstream/{repo}: no repository of this name in specs/config.toml (000048)")
    for repo, settings in sorted(upstream.items()):
        if not re.fullmatch(REPO, repo):
            errors.append(f"specs/config.toml: upstream {repo!r} is not <host>/<owner>/<repo> (000047)")
            continue
        if not isinstance(settings, dict) or not settings.get("ref"):
            errors.append(f"specs/config.toml: upstream {repo!r} must have ref (000048)")
            continue
        base = UPSTREAM / repo
        if repo not in copies:
            errors.append(f"specs/config.toml: upstream {repo!r} has no copy in specs/upstream/; run with --fetch (000048)")
            continue
        for path in sorted(base.rglob("*.md")):
            rel = path.relative_to(base)
            kind = _kind_of(rel)
            if kind is None or len(kind[2].parts) != 3 or not FILE_NAME.match(path.name):
                continue
            parsed = _parse_front_matter(path.read_text(encoding="utf-8"))
            status = str(parsed[0].get("status")) if parsed else ""
            below = kind[2]
            ids[f"{repo}:{kind[0]}/{below.parts[0]}/{below.parts[1]}/{path.name[:6]}"] = status
        exclude = settings.get("exclude", {})
        if not isinstance(exclude, dict):
            errors.append(f"specs/config.toml: exclude of {repo!r} must map rule IDs to reasons (000049)")
            continue
        for rule, reason in exclude.items():
            if f"{repo}:{rule}" not in ids:
                errors.append(f"specs/config.toml: excluded rule {rule!r} is not in the copy of {repo} (000049)")
            elif not isinstance(reason, str) or not reason.strip():
                errors.append(f"specs/config.toml: excluded rule {rule!r} needs a reason (000049)")
            else:
                ids[f"{repo}:{rule}"] = "excluded"
    return ids, errors


def _foreign_error(where: str, ref: str, foreign: dict[str, str]) -> str | None:
    """Return the error of one reference to a rule of a different repository, or None."""
    status = foreign.get(ref)
    if status is None:
        return f"{where}: {ref} names no rule in specs/upstream/ (000047)"
    if status == "excluded":
        return f"{where}: {ref} names an excluded rule (000049)"
    if status not in IN_FORCE:
        return f"{where}: {ref} names a rule that is not in force (000049)"
    return None


def _spec_foreign_refs(specs: list[Spec], foreign: dict[str, str]) -> list[str]:
    """Return the references in the specs to rules of a different repository that fail (000047)."""
    errors: list[str] = []
    for spec in specs:
        for repo, rule in FOREIGN_REF.findall(INLINE_CODE.sub("", spec.body)):
            error = _foreign_error(str(spec.rel), f"{repo}:{rule}", foreign)
            if error:
                errors.append(error)
    return errors


def fetch(config: dict[str, object]) -> list[str]:
    """Replace each copy below `specs/upstream/` with `specs/` of its repository at `ref` (000048)."""
    import shutil
    import tempfile

    errors: list[str] = []
    for repo, settings in sorted(config["upstream"].items()):  # type: ignore[union-attr]
        ref = settings.get("ref") if isinstance(settings, dict) else None
        if not ref:
            errors.append(f"specs/config.toml: upstream {repo!r} must have ref (000048)")
            continue
        with tempfile.TemporaryDirectory() as tmp:
            steps = [
                ["git", "init", "-q", tmp],
                ["git", "-C", tmp, "fetch", "-q", "--depth", "1", f"https://{repo}.git", str(ref)],
                ["git", "-C", tmp, "checkout", "-q", "FETCH_HEAD"],
            ]
            for step in steps:
                if subprocess.run(step, capture_output=True, text=True).returncode != 0:
                    errors.append(f"specs/config.toml: cannot fetch {repo} at {ref} (000048)")
                    break
            else:
                source = Path(tmp) / "specs"
                if not source.is_dir():
                    errors.append(f"{repo} at {ref} has no specs/ folder (000048)")
                    continue
                target = UPSTREAM / repo
                shutil.rmtree(target, ignore_errors=True)
                shutil.copytree(source, target, ignore=shutil.ignore_patterns("upstream"))
    return errors


def _code_refs(ids: dict[str, Spec], config: dict[str, object], foreign: dict[str, str]) -> list[str]:
    """Return the `§` references in the code that name no spec (000017, 000047)."""
    errors: list[str] = []
    suffixes = config["code_suffixes"]
    for folder in config["code_dirs"]:  # type: ignore[union-attr]
        for path in sorted((ROOT / folder).rglob("*")):
            if not path.is_file() or path.suffix not in suffixes or "node_modules" in path.parts:  # type: ignore[operator]
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for ref in SECTION_REF.findall(text):
                if ":" in ref:
                    error = _foreign_error(str(path.relative_to(ROOT)), ref, foreign)
                    if error:
                        errors.append(error)
                elif ref not in ids:
                    errors.append(f"{path.relative_to(ROOT)}: §{ref} names no spec (000017)")
    return errors


def _git_numbers(ref: str) -> dict[str, str] | None:
    """Return number to spec path at a git ref, or None when git cannot read the ref."""
    try:
        out = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", ref, "--", "specs"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    paths = [Path(line) for line in out.splitlines() if FILE_NAME.match(Path(line).name)]
    return {p.name[:6]: p.relative_to("specs").as_posix() for p in paths}


def _base_errors(numbers: dict[str, Path], base_ref: str) -> list[str]:
    """Return the numbers that the base branch gave to a different spec (000013).

    A number collides when the base branch added it after the branch left the base branch, and
    the working tree has it at a different path. A checkout without the ref checks nothing.
    """
    try:
        fork_ref = subprocess.run(
            ["git", "merge-base", "HEAD", base_ref],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return []
    base, fork = _git_numbers(base_ref), _git_numbers(fork_ref)
    if base is None or fork is None:
        return []
    return [
        f"{path}: number {number} is {base[number]} on {base_ref}; give the spec a new number (000013)"
        for number, path in sorted((n, p.as_posix()) for n, p in numbers.items())
        if number in base and number not in fork and base[number] != path
    ]


def main(argv: list[str]) -> int:
    """Run every check. Return 1 when one fails."""
    config = _config()
    if "--fetch" in argv:
        fetch_errors = fetch(config)
        for error in fetch_errors:
            print(error)
        if fetch_errors:
            return 1
    specs, errors = load()
    foreign, upstream_errors = _upstream_ids(config)
    errors += upstream_errors
    errors += _spec_foreign_refs(specs, foreign)
    ids = {s.full_id: s for s in specs}
    numbers: dict[str, Path] = {}
    for spec in specs:
        number = spec.path.name[:6]
        if number in numbers:
            errors.append(f"{spec.rel}: number used by {numbers[number]} (000013)")
        numbers[number] = spec.rel
        errors += _check_meta(spec, ids)
        errors += _check_body(spec, int(config["max_elements"]))  # type: ignore[arg-type]
    errors += _base_errors(numbers, str(config["base_ref"]))
    owned = {schema_path(s.path) for s in specs if s.prefix == "P"}
    if (SPECS / "protocols").is_dir():
        errors += [
            f"{p.relative_to(SPECS)}: no protocol spec owns this schema file (000028)"
            for p in sorted((SPECS / "protocols").rglob("*.json"))
            if p not in owned
        ]
    if "--write" in argv:
        README.write_text(_readme(specs), encoding="utf-8")
    elif README.read_text(encoding="utf-8") != _readme(specs):
        errors.append("specs/README.md: index or tree is not current; run with --write (000007)")
    errors += _code_refs(ids, config, foreign)
    for error in errors:
        print(error)
    print(f"{len(specs)} specs, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
