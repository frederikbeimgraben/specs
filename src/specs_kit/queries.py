"""The read commands that the command line and the MCP server share."""

from __future__ import annotations

from specs_kit.check import run
from specs_kit.new import kind_name
from specs_kit.project import KINDS_BY_PREFIX, Project, Spec


class QueryError(Exception):
    """A query names no rule."""


def find(project: Project, ref: str) -> Spec:
    """Return the spec of a short or a long ID.

    Args:
        project: The project.
        ref: The ID.

    Returns:
        The spec.

    Raises:
        QueryError: No rule has this ID.
    """
    spec = project.find(ref)
    if spec is None:
        raise QueryError(f"{ref} names no rule")
    return spec


def resolve(project: Project, ref: str) -> str:
    """Return the long form of a short or a long ID (§000047).

    Args:
        project: The project.
        ref: The ID.

    Returns:
        The long form.
    """
    return find(project, ref).long


def show(project: Project, ref: str) -> str:
    """Return the full text of a spec.

    Args:
        project: The project.
        ref: The short or the long ID.

    Returns:
        The text of the file.
    """
    return find(project, ref).path.read_text(encoding="utf-8")


def _line(spec: Spec) -> str:
    """Return one line of a list: kind letter, short form, status and title.

    Args:
        spec: The spec.

    Returns:
        The line.
    """
    return f"{spec.prefix}\t{spec.short}\t{spec.status}\t{spec.title}"


def rules(project: Project, kind: str | None = None) -> tuple[Spec, ...]:
    """Return the rules of the project and of the copies, optionally of one kind (§000072).

    Args:
        project: The project.
        kind: The kind name or the kind letter, or None for all kinds.

    Returns:
        The rules.
    """
    wanted = None if kind is None else kind_name(kind)
    return tuple(
        s for s in project.all_specs() if wanted is None or KINDS_BY_PREFIX.get(s.prefix) == wanted
    )


def listing(project: Project, kind: str | None = None) -> str:
    """Return one line for each rule of the project and of the copies, optionally of one kind.

    Args:
        project: The project.
        kind: The kind name or the kind letter, or None for all kinds.

    Returns:
        The lines.
    """
    return "".join(f"{_line(s)}\n" for s in rules(project, kind))


def matches(project: Project, text: str) -> tuple[Spec, ...]:
    """Return each rule whose title or text holds `text`, without case.

    Args:
        project: The project.
        text: The text to find.

    Returns:
        The rules.
    """
    needle = text.casefold()
    return tuple(
        s
        for s in project.all_specs()
        if needle in s.title.casefold() or needle in s.body.casefold()
    )


def search(project: Project, text: str) -> str:
    """Return one line for each rule whose title or text holds `text`, without case.

    Args:
        project: The project.
        text: The text to find.

    Returns:
        The lines.
    """
    return "".join(f"{_line(s)}\n" for s in matches(project, text))


def check(project: Project, *, write: bool = False) -> tuple[bool, str]:
    """Run the check.

    Args:
        project: The project.
        write: True to write the index and `AGENTS.md` first, as `specs install` does.

    Returns:
        True without errors, and the report.
    """
    count, errors = run(project, write=write)
    return not errors, "".join(f"{e}\n" for e in errors) + f"{count} specs, {len(errors)} errors\n"
