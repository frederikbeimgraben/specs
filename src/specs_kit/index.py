"""Write the text of the index `specs/README.md` (§000007)."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from specs_kit.project import IN_FORCE, KINDS, Project, Spec


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
                *(("  .upstream/", *(f"    {repo}/" for repo in copies)) if copies else ()),
            )
        )
        + "\n"
    )


def row(spec: Spec) -> str:
    """Return the index row of one spec, with a link from the root of the repository.

    Args:
        spec: The spec.

    Returns:
        The row.
    """
    folder = f"specs/.upstream/{spec.repo}" if spec.repo else "specs"
    return f"| [{spec.long}](/{folder}/{spec.rel.as_posix()}) | {spec.title} | {spec.status} |"


def index(
    project: Project, specs: tuple[Spec, ...], foreign: Mapping[str, str], copied: tuple[Spec, ...]
) -> str:
    """Return the text of the index `specs/README.md` (§000007).

    Args:
        project: The project.
        specs: The specs of the project.
        foreign: The status of each rule of the copies by short form.
        copied: The specs of the copies.

    Returns:
        The whole text of the index.
    """
    upstream = tuple(s for s in copied if foreign.get(s.short) in IN_FORCE)
    head = ("| ID | Title | Status |", "| --- | --- | --- |")
    return (
        "\n".join(
            (
                "# Specs",
                "",
                "The binding rules of this project. The kind folders of `specs/` hold the rules",
                "of the project, `specs/.upstream/` the rules of different repositories and",
                "`specs/.templates/` the templates. The command `specs install` writes this",
                "file. Do not change it by hand (000007).",
                "",
                "A new spec starts with",
                '`specs new <kind> <area>/<topic> <name> "<title>" --scope <path>` (000008).',
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
                *(row(s) for s in sorted(specs, key=lambda s: s.full_id)),
                "",
                "## Upstream",
                "",
                "The rules of different repositories that apply to this project (000049).",
                "",
                *(
                    (*head, *(row(s) for s in sorted(upstream, key=lambda s: s.long)))
                    if upstream
                    else ("No rules.",)
                ),
            )
        )
        + "\n"
    )
