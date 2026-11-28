"""Migration 5: give the files of the kit in a project the new name `spezi` (§000081).

The kit was `github.com/frederikbeimgraben/specs` with the command `specs`. Its files in a
project had this name too: `specs.toml`, `specs.lock`, the skills `spec-*`, the folders of the
editors, the CI file, the MCP server, the flake input and the markers of the block in
`AGENTS.md`. The migration gives each of them the new name. A CI file or a `flake.nix` moves
only when it holds the text of the kit, so that the change of a person stays.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from importlib import resources
from pathlib import Path
from typing import cast

from spezi.changes import delete_file, move_tree, write_text
from spezi.project import (
    CONFIG_NAME,
    KIT_REPO,
    OLD_CONFIG_NAME,
    OLD_KIT_REPO,
    UPSTREAM,
    hidden,
    read_config,
)

COMMIT = "a2580250777d900688fd985fa515bfc3effeb5de"
DESCRIPTION = "give the files of the kit the new name spezi"
OLD_NAME = "specs"
NEW_NAME = "spezi"
FILES: Mapping[str, str] = {OLD_CONFIG_NAME: CONFIG_NAME, "specs.lock": "spezi.lock"}
SKILLS = ("adopt", "approve", "check", "structure", "write")
FOLDERS: Mapping[str, str] = {
    ".zed/specs": ".zed/spezi",
    ".vscode/specs": ".vscode/spezi",
    **{f".claude/skills/spec-{s}": f".claude/skills/spezi-{s}" for s in SKILLS},
}
CI_FILES: Mapping[str, tuple[str, str]] = {
    ".github/workflows/specs.yml": ("github-workflow.yml", ".github/workflows/spezi.yml"),
    ".gitlab/ci/specs.yml": ("gitlab-ci.yml", ".gitlab/ci/spezi.yml"),
    ".forgejo/workflows/specs.yml": ("codeberg-workflow.yml", ".forgejo/workflows/spezi.yml"),
}
GITLAB_INCLUDE: Mapping[str, str] = {
    "  - local: .gitlab/ci/specs.yml": "  - local: .gitlab/ci/spezi.yml"
}
OLD_LONG_ID = re.compile(rf"(?<![\w./-]){re.escape(OLD_KIT_REPO)}(?=:)")
OLD_BEGIN = re.compile(r"^<!-- specs:begin \(written by [^)]*\) -->$", re.MULTILINE)
OLD_END = "<!-- specs:end -->"
BEGIN = "<!-- spezi:begin (written by spezi install, do not edit) -->"
END = "<!-- spezi:end -->"


def _data(name: str) -> str:
    """Return the text of a file of the package data.

    Args:
        name: The file name below `spezi/data/`.

    Returns:
        The text.
    """
    return resources.files("spezi").joinpath("data", name).read_text(encoding="utf-8")


def _old_form(template: str) -> re.Pattern[str]:
    """Return the pattern of the text that the old kit wrote from a template of the new kit.

    The old text is the new text with the old name. The placeholders `{ref}` and `{branch}` match
    each value.

    Args:
        template: The text of the template of the new kit.

    Returns:
        The pattern with the groups `ref` and `branch` where the template has them.
    """
    old = re.escape(template.replace(NEW_NAME, OLD_NAME))
    return re.compile(
        old.replace(re.escape("{ref}"), r"(?P<ref>[^\s\"/]+)", 1)
        .replace(re.escape("{ref}"), r"(?P=ref)")
        .replace(re.escape("{branch}"), r"(?P<branch>[^\]\s]+)", 1)
    )


def _replace_in(path: Path, change: Mapping[str, str]) -> None:
    """Replace texts in a file when the file exists.

    Args:
        path: The file.
        change: The new text for each old text.
    """
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    new = text
    for old, replacement in change.items():
        new = new.replace(old, replacement)
    if new != text:
        write_text(path, new)


def _move(root: Path, old: str, new: str) -> None:
    """Move a file or a folder to its new name when the new name does not exist.

    Args:
        root: The root of the project.
        old: The old path from the root.
        new: The new path from the root.
    """
    source, target = root / old, root / new
    match source.is_dir(), source.is_file(), target.exists():
        case True, _, False:
            move_tree(source, target)
        case False, True, False:
            write_text(target, source.read_text(encoding="utf-8"))
            delete_file(source)
        case _:
            pass


def _long_ids(path: Path) -> None:
    """Give each long ID of the kit in a file the new name of the kit.

    Args:
        path: The file.
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    new = OLD_LONG_ID.sub(KIT_REPO, text)
    if new != text:
        write_text(path, new)


def _ci(root: Path) -> None:
    """Move each CI file of the kit that holds the text of the old kit.

    Args:
        root: The root of the project.
    """
    for old, (data, new) in CI_FILES.items():
        path = root / old
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        found = _old_form(_data(data)).fullmatch(text) if text else None
        if found and not (root / new).exists():
            write_text(root / new, text.replace(OLD_NAME, NEW_NAME))
            delete_file(path)
    _replace_in(root / ".gitlab-ci.yml", GITLAB_INCLUDE)


def _renamed(node: Mapping[str, object]) -> dict[str, object]:
    """Return a node of `flake.lock` with the new name of the repository.

    Args:
        node: The node of the kit.

    Returns:
        The node with the new `repo` in `locked` and in `original`.
    """
    return {
        key: (
            {**cast("dict[str, object]", value), "repo": NEW_NAME}
            if key in ("locked", "original") and isinstance(value, dict)
            else value
        )
        for key, value in node.items()
    }


def _flake_lock(path: Path) -> None:
    """Give the input of the kit in `flake.lock` the new name. The commit stays.

    Args:
        path: The file `flake.lock`.
    """
    data = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    nodes = cast("dict[str, dict[str, object]]", data.get("nodes", {}))
    top = str(data.get("root", "root"))
    inputs = cast("dict[str, str]", nodes.get(top, {}).get("inputs", {}))
    if inputs.get(OLD_NAME) != OLD_NAME or OLD_NAME not in nodes or NEW_NAME in nodes:
        return
    new_nodes = {
        **{name: node for name, node in nodes.items() if name != OLD_NAME},
        NEW_NAME: _renamed(nodes[OLD_NAME]),
        top: {
            **nodes[top],
            "inputs": {
                (NEW_NAME if name == OLD_NAME else name): (NEW_NAME if node == OLD_NAME else node)
                for name, node in inputs.items()
            },
        },
    }
    write_text(path, json.dumps({**data, "nodes": new_nodes}, indent=2, sort_keys=True) + "\n")


def _flake(root: Path) -> None:
    """Give the input of the kit in `flake.nix` and `flake.lock` the new name.

    The files change only when `flake.nix` holds the text of the old kit.

    Args:
        root: The root of the project.
    """
    path = root / "flake.nix"
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    if text and _old_form(_data("flake.nix")).fullmatch(text):
        write_text(path, text.replace(OLD_NAME, NEW_NAME))
        _flake_lock(root / "flake.lock")


def _mcp(root: Path) -> None:
    """Give the MCP server of the kit in `.mcp.json` the new name.

    Args:
        root: The root of the project.
    """
    path = root / ".mcp.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except json.JSONDecodeError:
        return
    servers = data.get("mcpServers") if isinstance(data, dict) else None
    if not isinstance(servers, dict) or OLD_NAME not in servers or NEW_NAME in servers:
        return
    renamed = {(NEW_NAME if k == OLD_NAME else k): v for k, v in servers.items()}
    write_text(path, json.dumps({**data, "mcpServers": renamed}, indent=2) + "\n")


def _ignore_line(line: str) -> str:
    """Return a line of `.gitignore` with the new name of the folder of an editor.

    Args:
        line: The line.

    Returns:
        The line with the new folder, or the line as it is.
    """
    name = line.strip("/")
    return line.replace(name, FOLDERS[name]) if name in (".zed/specs", ".vscode/specs") else line


def _gitignore(root: Path) -> None:
    """Give the folders of the editors in `.gitignore` the new name.

    Args:
        root: The root of the project.
    """
    path = root / ".gitignore"
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    new = "\n".join(_ignore_line(line) for line in text.split("\n"))
    if new != text:
        write_text(path, new)


def _agents(root: Path) -> None:
    """Give the markers of the block in `AGENTS.md` the new name.

    Args:
        root: The root of the project.
    """
    path = root / "AGENTS.md"
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    new = "\n".join(
        END if line == OLD_END else line for line in OLD_BEGIN.sub(BEGIN, text).split("\n")
    )
    if new != text:
        write_text(path, new)


def _specs_and_code(root: Path) -> None:
    """Give the long IDs of the kit in the specs and in the code of the project the new name.

    Args:
        root: The root of the project.
    """
    specs = root / "specs"
    config = read_config(root / CONFIG_NAME)
    code = (
        p
        for folder in config.code_dirs
        for p in sorted((root / folder).rglob("*"))
        if p.is_file() and p.suffix in config.code_suffixes
    )
    rules = (
        p for p in sorted(specs.rglob("*.md")) if p.is_file() and not hidden(p.relative_to(specs))
    )
    for path in (*rules, *code):
        _long_ids(path)


def project(root: Path) -> None:
    """Give each file of the kit in the project the new name.

    Args:
        root: The root of the project.
    """
    for old, new in FILES.items():
        _move(root, old, new)
        _replace_in(root / new, {f'"{OLD_KIT_REPO}"': f'"{KIT_REPO}"'})
    _move(root, f"specs/{UPSTREAM}/{OLD_KIT_REPO}", f"specs/{UPSTREAM}/{KIT_REPO}")
    for old, new in FOLDERS.items():
        _move(root, old, new)
    _gitignore(root)
    _ci(root)
    _flake(root)
    _mcp(root)
    _agents(root)
    _specs_and_code(root)


def copy(folder: Path) -> None:
    """Give the long IDs of the kit in the rules of a copy the new name.

    Args:
        folder: The folder of the copy.
    """
    for path in sorted(p for p in folder.rglob("*.md") if p.is_file()):
        _long_ids(path)
