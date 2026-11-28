"""`spezi install`: bring a project to the state of its `spezi.toml` and `spezi.lock` (spec 000083).

The command changes no pin. It runs the migrations, loads each copy that does not agree with
`spezi.lock`, writes each missing file of the kit and keeps each file that exists.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from contextlib import ExitStack
from pathlib import Path
from typing import cast

from spezi.agents import AGENTS, BLOCK, CLAUDE, IMPORT, claude_import
from spezi.changes import MIGRATED, delete_file, remove_tree, write_text
from spezi.devshell import ENVRC, FLAKE, INPUT, LOCK, envrc, flake_template
from spezi.kit import (
    CI_FILES,
    GITLAB_INCLUDE,
    GITLAB_ROOT,
    MCP_NAME,
    check_forge,
    check_program,
    checkout,
    gitlab_root_text,
    lazy_history,
    own_ref,
    package_data,
    read_mcp,
    skills,
    sync_copies,
    sync_transitive,
    templates,
    write_mcp,
)
from spezi.lock import read_lock
from spezi.migrations import migrate_project
from spezi.project import (
    ATTRIBUTES_NAME,
    KIT_REPO,
    UPSTREAM_ATTRIBUTE,
    Project,
    kit_rev,
    kit_source,
)
from spezi.refs import for_project


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
    """Return the template files, and the skill files when `skills` is on, that are missing.

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
            for skill in (skills(source) if project.config.on("skills") else ())
            for rel in _files(skill)
        ),
    )
    return tuple((src, dst) for src, dst in pairs if not dst.exists())


def _kit_text(project: Project, src: Path, dst: Path) -> str:
    """Return the text of a file of the kit for the project.

    Args:
        project: The project.
        src: The file of the kit.
        dst: The file of the project.

    Returns:
        The text. A skill gets the foreign short form of the rules of the kit (spec 000017).
    """
    text = src.read_text(encoding="utf-8")
    skill = dst.is_relative_to(project.root / ".claude" / "skills") and dst.suffix == ".md"
    return for_project(project.upstream_dir, text) if skill else text


def _kit_files(project: Project, commit: str) -> None:
    """Write each missing template, and each missing skill, CI file and MCP entry that is on.

    The files come from this program when it is the kit at `commit`, else from a checkout of the
    kit at `commit`, which the command fetches only when a file is missing.

    Args:
        project: The project.
        commit: The commit of the kit in `spezi.lock`.
    """
    forge = project.config.forge
    check_forge(project.root, forge, project.config.on("ci"))
    with ExitStack() as stack:
        source = (
            kit_source()
            if kit_rev() == commit or not _missing(kit_source(), project)
            else stack.enter_context(checkout(KIT_REPO, commit))
        )
        for src, dst in _missing(source, project):
            write_text(dst, _kit_text(project, src, dst))
    data_name, target = CI_FILES[forge]
    branch = project.config.base_ref.removeprefix("origin/")
    if project.config.on("ci") and not (project.root / target).exists():
        write_text(
            project.root / target,
            package_data(data_name).replace("{ref}", commit).replace("{branch}", branch),
        )
    root_text = (
        gitlab_root_text(project.root) if forge == "gitlab" and project.config.on("ci") else None
    )
    if root_text is not None:
        write_text(project.root / GITLAB_ROOT, root_text)
    mcp = project.root / ".mcp.json"
    if project.config.on("mcp") and MCP_NAME not in cast(
        "dict[str, object]", read_mcp(mcp).get("mcpServers", {})
    ):
        write_mcp(project, commit)


def _add_attribute(project: Project) -> None:
    """Add the line for the copies to `.gitattributes` when it is missing (spec 000048).

    Args:
        project: The project.
    """
    path = project.root / ATTRIBUTES_NAME
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    if project.needs_attribute():
        write_text(
            path,
            "".join(
                (text, "\n" if text and not text.endswith("\n") else "", UPSTREAM_ATTRIBUTE, "\n")
            ),
        )


def install(project: Project) -> tuple[str, ...]:
    """Bring a project to the state of `spezi.toml` and `spezi.lock`, without a change of a pin.

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
        copied = (*sync_copies(fresh, history), *sync_transitive(fresh, history))
    _add_attribute(fresh)
    locked = read_lock(fresh.root).get(KIT_REPO)
    if locked is not None:
        _kit_files(fresh, locked.commit)
    config = fresh.config
    return (
        *(f"{MIGRATED}{d}" for d in dict.fromkeys((*ran, *copied))),
        *(envrc(fresh.root) if locked is not None and config.on("envrc") else ()),
        *(claude_import(fresh.root) if config.on("claude") else ()),
        *(remove_off(fresh, locked.commit) if locked is not None else ()),
    )


def _remove_file(path: Path, kit_text: str, hint: str) -> tuple[str, ...]:
    """Delete a file that holds only the text of the kit, else give a hint.

    Args:
        path: The file.
        kit_text: The text that the kit writes.
        hint: The hint for a file with a different text.

    Returns:
        The hint, or nothing when the file does not exist or is deleted.
    """
    match path.is_file(), path.is_file() and path.read_text(encoding="utf-8") == kit_text:
        case False, _:
            return ()
        case True, True:
            delete_file(path)
            return ()
        case _:
            return (hint,)


def _remove_mcp(path: Path) -> None:
    """Remove the server `spezi` from `.mcp.json`. Delete the file when nothing stays.

    Args:
        path: The file `.mcp.json`.
    """
    data = read_mcp(path)
    servers = cast("dict[str, object]", data.get("mcpServers", {}))
    if MCP_NAME not in servers:
        return
    rest = {k: v for k, v in servers.items() if k != MCP_NAME}
    kept = (
        {**data, "mcpServers": rest}
        if rest
        else {k: v for k, v in data.items() if k != "mcpServers"}
    )
    match kept:
        case {}:
            delete_file(path)
        case _:
            write_text(path, json.dumps(kept, indent=2) + "\n")


def _remove_block(path: Path) -> None:
    """Remove the block of the kit from `AGENTS.md`. Delete the file when nothing stays.

    Args:
        path: The file `AGENTS.md`.
    """
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    if not BLOCK.search(text):
        return
    rest = BLOCK.sub("", text).strip()
    match rest:
        case "":
            delete_file(path)
        case _:
            write_text(path, f"{rest}\n")


def _remove_gitlab_include(root: Path) -> None:
    """Remove the include of the kit job from `.gitlab-ci.yml`, and `include:` when it is empty.

    Args:
        root: The root of the project.
    """
    path = root / GITLAB_ROOT
    lines = path.read_text(encoding="utf-8").splitlines() if path.is_file() else []
    if GITLAB_INCLUDE not in lines:
        return
    rest = [ln for ln in lines if ln != GITLAB_INCLUDE]
    at = rest.index("include:") if "include:" in rest else -1
    empty = at >= 0 and not (at + 1 < len(rest) and rest[at + 1].startswith("  "))
    kept = "\n".join(ln for i, ln in enumerate(rest) if not (empty and i == at)).strip()
    match kept:
        case "":
            delete_file(path)
        case _:
            write_text(path, f"{kept}\n")


def remove_off(project: Project, commit: str) -> tuple[str, ...]:
    """Remove each part of the kit whose switch in `[features]` is off (spec 000084).

    `flake.nix`, `.envrc` and `CLAUDE.md` go away only when they hold only the text of the kit.
    Else the command gives a hint with what to remove by hand.

    Args:
        project: The project.
        commit: The commit of the kit in `spezi.lock`.

    Returns:
        The hints.
    """
    config = project.config
    root = project.root
    if not config.on("skills"):
        for folder in sorted((root / ".claude" / "skills").glob("spezi-*")):
            remove_tree(folder)
        for empty in (root / ".claude" / "skills", root / ".claude"):
            if empty.is_dir() and not any(empty.iterdir()):
                empty.rmdir()
    if not config.on("ci"):
        for _, target in CI_FILES.values():
            delete_file(root / target)
        _remove_gitlab_include(root)
    if not config.on("mcp"):
        _remove_mcp(root / ".mcp.json")
    if not config.on("agents"):
        _remove_block(root / AGENTS)
    return (
        *(
            ()
            if config.on("claude")
            else _remove_file(
                root / CLAUDE, f"{IMPORT}\n", f"hint: remove the line {IMPORT} from {CLAUDE}"
            )
        ),
        *(() if config.on("flake") else _remove_flake(root, commit)),
        *(
            ()
            if config.on("envrc")
            else _remove_file(
                root / ENVRC, "use flake\n", f"hint: remove the line use flake from {ENVRC}"
            )
        ),
    )


def _remove_flake(root: Path, commit: str) -> tuple[str, ...]:
    """Delete `flake.nix` and `flake.lock` when `flake.nix` is the flake of the kit.

    Args:
        root: The root of the project.
        commit: The commit of the kit.

    Returns:
        A hint when `flake.nix` has a different text and the input `spezi`.
    """
    path = root / FLAKE
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    match text == flake_template(commit), bool(INPUT.search(text)):
        case True, _:
            delete_file(path)
            delete_file(root / LOCK)
            return ()
        case False, True:
            return (f"hint: remove the input spezi and its package from {FLAKE}",)
        case _:
            return ()
