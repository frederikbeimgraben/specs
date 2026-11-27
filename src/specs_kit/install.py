"""`specs install`: bring a project to the state of its `specs.toml` and `specs.lock` (§000083).

The command changes no pin. It runs the migrations, loads each copy that does not agree with
`specs.lock`, writes each missing file of the kit and keeps each file that exists.
"""

from __future__ import annotations

from collections.abc import Iterable
from contextlib import ExitStack
from pathlib import Path

from specs_kit.agents import claude_import
from specs_kit.changes import write_text
from specs_kit.devshell import envrc
from specs_kit.kit import (
    CI_FILES,
    GITLAB_ROOT,
    check_forge,
    check_program,
    checkout,
    gitlab_root_text,
    lazy_history,
    own_ref,
    package_data,
    skills,
    sync_copies,
    templates,
    write_mcp,
)
from specs_kit.lock import drop_locked, read_lock
from specs_kit.migrations import migrate_project
from specs_kit.project import KIT_REPO, Project, kit_rev, kit_source


def _files(folder: Path) -> tuple[Path, ...]:
    """Return the files below a folder, relative to it.

    Args:
        folder: The folder.

    Returns:
        The paths, sorted.
    """
    return tuple(
        sorted(p.relative_to(folder) for p in folder.rglob("*") if p.is_file())
        if folder.is_dir()
        else ()
    )


def _missing(source: Path, project: Project) -> tuple[tuple[Path, Path], ...]:
    """Return the template and skill files of the kit that the project does not have.

    Args:
        source: The root of the kit.
        project: The project.

    Returns:
        The source file and the target file of each missing file.
    """
    pairs: Iterable[tuple[Path, Path]] = (
        *(
            (templates(source) / rel, project.templates_dir / rel)
            for rel in _files(templates(source))
        ),
        *(
            (skill / rel, project.root / ".claude" / "skills" / skill.name / rel)
            for skill in skills(source)
            for rel in _files(skill)
        ),
    )
    return tuple((src, dst) for src, dst in pairs if not dst.exists())


def _kit_files(project: Project, commit: str) -> None:
    """Write each missing template, skill, CI file and the MCP server entry of the kit.

    The files come from this program when it is the kit at `commit`, else from a checkout of the
    kit at `commit`, which the command fetches only when a file is missing.

    Args:
        project: The project.
        commit: The commit of the kit in `specs.lock`.
    """
    forge = project.config.forge
    check_forge(project.root, forge)
    with ExitStack() as stack:
        source = (
            kit_source()
            if kit_rev() == commit or not _missing(kit_source(), project)
            else stack.enter_context(checkout(KIT_REPO, commit))
        )
        for src, dst in _missing(source, project):
            write_text(dst, src.read_text(encoding="utf-8"))
    data_name, target = CI_FILES[forge]
    branch = project.config.base_ref.removeprefix("origin/")
    if not (project.root / target).exists():
        write_text(
            project.root / target,
            package_data(data_name).replace("{ref}", commit).replace("{branch}", branch),
        )
    root_text = gitlab_root_text(project.root) if forge == "gitlab" else None
    if root_text is not None:
        write_text(project.root / GITLAB_ROOT, root_text)
    mcp = project.root / ".mcp.json"
    if not mcp.is_file() or '"specs"' not in mcp.read_text(encoding="utf-8"):
        write_mcp(project, commit)


def install(project: Project) -> tuple[str, ...]:
    """Bring a project to the state of `specs.toml` and `specs.lock`, without a change of a pin.

    Args:
        project: The project.

    Returns:
        The hints: one line `migrated: <description>` for each migration that ran, and the lines
        to add to an existing `.envrc` or `CLAUDE.md`.
    """
    with lazy_history() as history:
        own = own_ref(project)
        check_program(history, own)
        ran = () if own is None else migrate_project(history, project.root, own)
        fresh = Project.open(project.root)
        copied = sync_copies(fresh, history)
    drop_locked(fresh.root, frozenset(fresh.config.upstream))
    locked = read_lock(fresh.root).get(KIT_REPO)
    if locked is not None:
        _kit_files(fresh, locked.commit)
    return (
        *(f"migrated: {d}" for d in dict.fromkeys((*ran, *copied))),
        *(envrc(fresh.root) if locked is not None else ()),
        *claude_import(fresh.root),
    )
