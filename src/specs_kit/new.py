"""Create a new spec from its template (§000008)."""

from __future__ import annotations

import datetime
import re
import subprocess
from collections.abc import Mapping
from pathlib import Path

from specs_kit.check import git_numbers
from specs_kit.project import FOLDER, FOLDER_BY_KIND, KINDS_BY_PREFIX, Project


class NewError(Exception):
    """A new spec cannot be created."""


TEMPLATES: Mapping[str, str] = {
    "protocol": "TEMPLATE-protocol.md",
    "structure": "TEMPLATE-structure.md",
    "decision": "TEMPLATE-decision.md",
}


def kind_name(kind: str) -> str:
    """Return the kind name of a kind name or a kind letter.

    Args:
        kind: For example `convention` or `C`.

    Returns:
        The kind name.

    Raises:
        NewError: The kind is unknown.
    """
    found = KINDS_BY_PREFIX.get(kind.upper(), kind)
    if found not in FOLDER_BY_KIND:
        raise NewError(f"unknown kind {kind!r}; use one of {', '.join(FOLDER_BY_KIND)}")
    return found


def git_owner(project: Project) -> str | None:
    """Return the login of `git config <forge>.user`, or None.

    Args:
        project: The project.

    Returns:
        The login, or None.
    """
    try:
        out = subprocess.run(
            ["git", "config", f"{project.config.forge}.user"],
            cwd=project.root,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    return out or None


def next_number(project: Project) -> str:
    """Return the highest number of the project and the base branch plus one (§000013).

    Args:
        project: The project.

    Returns:
        The six-digit number.
    """
    local = (s.number for s in project.load()[0])
    base = git_numbers(project, project.config.base_ref) or {}
    return f"{max((int(n) for n in (*local, *base)), default=0) + 1:06d}"


def fill(template: str, number: str, title: str, kind: str, owner: str, day: str) -> str:
    """Return the text of a template with the values of the new spec.

    Args:
        template: The text of the template.
        number: The six-digit number.
        title: The title.
        kind: The kind name.
        owner: The login of the owner.
        day: The date as `YYYY-MM-DD`.

    Returns:
        The text of the new spec.
    """
    values = {
        r"^id: .*$": f'id: "{number}"',
        r"^title: .*$": f"title: {title}",
        r"^kind: .*$": f"kind: {kind}",
        r"^owner: .*$": f"owner: {owner}",
        r"^updated: .*$": f"updated: {day}",
    }
    head, sep, body = template.partition("\n---\n")
    filled = "".join(
        next((re.sub(p, v, line) for p, v in values.items() if re.match(p, line)), line)
        for line in head.splitlines(keepends=True)
    )
    return filled + sep + re.sub(r"^# .*$", f"# {title}", body, count=1, flags=re.MULTILINE)


def new(project: Project, kind: str, path: str, name: str, title: str, owner: str | None) -> Path:
    """Create a new spec and return its path.

    Args:
        project: The project.
        kind: The kind name or the kind letter.
        path: `<area>/<topic>`.
        name: The short name of the file, in kebab case.
        title: The title.
        owner: The login of the owner, or None for `git config <forge>.user`.

    Returns:
        The path of the new file.

    Raises:
        NewError: A value is not valid, or no owner is known.
    """
    found = kind_name(kind)
    parts = tuple(path.strip("/").split("/"))
    login = owner or git_owner(project)
    if len(parts) != 2 or not all(FOLDER.match(p) for p in parts):
        raise NewError(f"{path!r} must be <area>/<topic> in kebab case (000005)")
    if not FOLDER.match(name):
        raise NewError(f"{name!r} must be kebab case (000016)")
    if login is None:
        raise NewError(f"no owner: pass --owner or set git config {project.config.forge}.user")
    template = project.templates_dir / TEMPLATES.get(found, "TEMPLATE.md")
    if not template.is_file():
        raise NewError(f"{template.relative_to(project.root)} does not exist; run specs update")
    number = next_number(project)
    target = project.specs_dir / FOLDER_BY_KIND[found] / parts[0] / parts[1] / f"{number}_{name}.md"
    text = fill(
        template.read_text(encoding="utf-8"),
        number,
        title,
        found,
        login,
        datetime.date.today().isoformat(),
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    return target
