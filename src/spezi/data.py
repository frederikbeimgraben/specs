"""The JSON forms of the output of the command `spezi` (§000080)."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping

from spezi.changes import Mark
from spezi.check import Count
from spezi.project import Project, Spec

type Json = None | bool | int | str | list[Json] | dict[str, Json]

ERROR = re.compile(
    r"^(?:(?P<file>[^\s:][^:]*?)(?::(?P<line>[0-9]+))?: )?"
    r"(?P<message>.*?)(?: \((?P<rule>[0-9]{6})\))?$"
)


def dumps(value: Json) -> str:
    """Return a JSON value as text, indented with two spaces.

    Args:
        value: The value.

    Returns:
        The text with a newline at the end.
    """
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def rule(project: Project, spec: Spec) -> Json:
    """Return one rule as in `spezi list`, with its long form and its path.

    Args:
        project: The project.
        spec: The spec.

    Returns:
        The object.
    """
    return {
        "kind": spec.prefix,
        "id": spec.short,
        "long": spec.long,
        "status": spec.status,
        "title": spec.title,
        "path": spec.path.resolve().relative_to(project.root.resolve()).as_posix(),
    }


def _value(value: str | tuple[str, ...]) -> Json:
    """Return one value of the front matter as JSON.

    Args:
        value: The value.

    Returns:
        A list for a list, None for `null`, else the text.
    """
    match value:
        case tuple():
            return list(value)
        case "null":
            return None
        case _:
            return value


def spec_text(project: Project, spec: Spec) -> Json:
    """Return one spec with its front matter as an object and its body.

    Args:
        project: The project.
        spec: The spec.

    Returns:
        The object.
    """
    return {
        "long": spec.long,
        "path": spec.path.resolve().relative_to(project.root.resolve()).as_posix(),
        "meta": {key: _value(spec.meta[key]) for key in spec.keys if key in spec.meta},
        "body": spec.body,
    }


def error(line: str) -> Json:
    """Return one error of the check as an object with its file, line, message and rule.

    Args:
        line: The error line.

    Returns:
        The object. `file`, `line` or `rule` is None when the error has none.
    """
    found = ERROR.match(line)
    return {
        "file": found["file"] if found else None,
        "line": int(found["line"]) if found and found["line"] else None,
        "message": found["message"] if found else line,
        "rule": found["rule"] if found else None,
    }


def report(count: Count, errors: tuple[str, ...]) -> dict[str, Json]:
    """Return the report of the check.

    Args:
        count: The counts of the rules of the project and of the copies.
        errors: The error lines.

    Returns:
        The object.
    """
    return {
        "specs": count.specs,
        "upstream": count.upstream,
        "errors": [error(e) for e in errors],
    }


def changed(lines: tuple[tuple[Mark, str], ...]) -> Json:
    """Return the changed files.

    Args:
        lines: The mark and the path of each change.

    Returns:
        The list of objects.
    """
    return [{"mark": str(mark), "path": path} for mark, path in lines]


def result(
    message: str, hints: tuple[str, ...], check: Json, files: tuple[tuple[Mark, str], ...]
) -> Mapping[str, Json]:
    """Return the result of a command that changes files.

    Args:
        message: The message of the command.
        hints: The hints.
        check: The report of the check, or None.
        files: The changed files.

    Returns:
        The object.
    """
    return {"message": message, "hints": list(hints), "check": check, "changed": changed(files)}
