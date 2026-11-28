"""Compare two versions of a copy before `update` or `add` replaces it (spec 000085).

The summary lists each new, changed and removed rule. `update` also finds the project rules
that refer to a rule that the new version replaces or removes, and the templates and skills that
a person changed.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from spezi.check import FOREIGN_REF
from spezi.context import where
from spezi.project import IN_FORCE, Project, Spec, hidden, parse_spec
from spezi.refs import INLINE_CODE

type Change = tuple[str, str, str]


def rules_in(
    folder: Path, repo: str, include: tuple[str, ...] = (), own: tuple[str, ...] = ()
) -> Mapping[str, Spec]:
    """Return the rules of a `specs/` folder by their number.

    Args:
        folder: The folder that holds the kind folders.
        repo: The repository of the rules.
        include: The folders below `folder` to read, or empty for all.
        own: The folders below `folder` that a copy leaves out (spec 000048).

    Returns:
        The spec of each number.
    """
    files = (
        sorted(
            p
            for p in folder.rglob("*.md")
            if p.parent != folder
            and not hidden(p.relative_to(folder))
            and (
                not include
                or any(p.relative_to(folder).as_posix().startswith(f"{f}/") for f in include)
            )
            and not any(p.relative_to(folder).as_posix().startswith(f"{o}/") for o in own)
        )
        if folder.is_dir()
        else ()
    )
    parsed = (parse_spec(p, folder, repo) for p in files)
    return {spec.number: spec for spec, errors in parsed if spec and not errors}


def rule_changes(old: Mapping[str, Spec], new: Mapping[str, Spec]) -> tuple[Change, ...]:
    """Return each new, changed and removed rule.

    Args:
        old: The rules of the copy now.
        new: The rules of the new version.

    Returns:
        The mark `A`, `M` or `D`, the number and the title of each change, sorted by number.
    """
    return tuple(
        sorted(
            (
                *(("A", n, s.title) for n, s in new.items() if n not in old),
                *(
                    ("M", n, s.title)
                    for n, s in new.items()
                    if n in old
                    and s.path.read_text(encoding="utf-8")
                    != old[n].path.read_text(encoding="utf-8")
                ),
                *(("D", n, s.title) for n, s in old.items() if n not in new),
            ),
            key=lambda c: c[1],
        )
    )


def change_lines(
    repo: str, old_ref: str | None, new_ref: str, commit: str, changes: tuple[Change, ...]
) -> str:
    """Return the summary of one repository.

    Args:
        repo: The repository.
        old_ref: The ref now, or None for a new copy.
        new_ref: The new ref.
        commit: The commit of the new ref.
        changes: The changed rules.

    Returns:
        The lines of the summary.
    """
    head = f"{repo}: {old_ref or '-'} -> {new_ref} ({commit[:12]})"
    body = tuple(f"  {mark} {number} {title}" for mark, number, title in changes)
    return "\n".join((head, *(body or ("  no rule changes",))))


def _targets(spec: Spec, repo: str) -> tuple[str, ...]:
    """Return the numbers of the rules of one repository that a spec names.

    Args:
        spec: The spec of the project.
        repo: The repository.

    Returns:
        The numbers from `replaces` and from the references in the text.
    """
    text = INLINE_CODE.sub("", spec.body)
    return tuple(
        dict.fromkeys(
            (
                *(
                    entry.partition(":")[2]
                    for entry in spec.entries("replaces") or ()
                    if entry.startswith(f"{repo}:")
                ),
                *(number for found, number in FOREIGN_REF.findall(text) if found == repo),
            )
        )
    )


def broken_references(project: Project, repo: str, new: Mapping[str, Spec]) -> tuple[str, ...]:
    """Return each reference of a project rule to a rule that the new version replaces or removes.

    Args:
        project: The project.
        repo: The repository.
        new: The rules of the new version.

    Returns:
        One line for each reference.
    """
    return tuple(
        f"{where(project, spec)}: {repo}:{number} is "
        + ("removed" if number not in new else new[number].status)
        for spec in project.load()[0]
        if spec.status in IN_FORCE
        for number in _targets(spec, repo)
        if number not in new or new[number].status not in IN_FORCE
    )
