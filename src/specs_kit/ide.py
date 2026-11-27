"""`specs setup-ide`: write the extension of the language server for Zed or VS Code (§000089).

The folder `.zed/specs/` holds the source of the Zed extension, and `.vscode/specs/` holds the
`.vsix` that the flake of the kit builds. Both hold `server.json` with the path of this program
and the suffixes of the code. The folder stays out of git.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Mapping
from pathlib import Path

from specs_kit.ask import Ask
from specs_kit.changes import replace_tree_all, write_text
from specs_kit.kit import KitError
from specs_kit.project import Project

FOLDERS: Mapping[str, str] = {"zed": ".zed/specs", "code": ".vscode/specs"}
ZED_LANGUAGES: Mapping[str, str] = {
    ".py": "Python",
    ".ts": "TypeScript",
    ".js": "JavaScript",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
    ".kt": "Kotlin",
    ".nix": "Nix",
    ".sh": "Shell Script",
}
ZED_SOURCE = Path(__file__).parent / "data" / "editors" / "zed"
VSIX = "specs.vsix"


def vsix() -> Path | None:
    """Return the `.vsix` of the VS Code extension that the flake of the kit built.

    Returns:
        The file of `SPECS_VSIX`, or None when the program has none.
    """
    path = Path(os.environ.get("SPECS_VSIX", ""))
    return path if path.name and path.is_file() else None


def program() -> str:
    """Return the absolute path of the `specs` program that runs.

    Returns:
        The path of the program, else of `specs` on `PATH`, else `specs`.
    """
    started = Path(sys.argv[0])
    return str(started.absolute()) if started.name == "specs" else shutil.which("specs") or "specs"


def server_json(project: Project) -> str:
    """Return the text of `server.json`.

    Args:
        project: The project.

    Returns:
        The JSON with `command` and `suffixes`.
    """
    data = {"command": program(), "suffixes": sorted(project.config.code_suffixes)}
    return json.dumps(data, indent=2) + "\n"


def zed_languages(suffixes: tuple[str, ...]) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Return the language names of Zed for the suffixes, with Markdown first.

    Args:
        suffixes: The suffixes of the code.

    Returns:
        The language names, and a hint for each suffix without a name.
    """
    return (
        tuple(
            dict.fromkeys(("Markdown", *(ZED_LANGUAGES[s] for s in suffixes if s in ZED_LANGUAGES)))
        ),
        tuple(
            f"{s}: Zed has no language name for this suffix; the extension skips it"
            for s in suffixes
            if s not in ZED_LANGUAGES
        ),
    )


def _copy_plain(source: Path, target: Path) -> None:
    """Copy the files of a folder without their modes, so that a copy from the Nix store can change.

    Args:
        source: The folder to copy.
        target: The folder of the copy.
    """
    for path in sorted(p for p in source.rglob("*") if p.is_file()):
        copy = target / path.relative_to(source)
        copy.parent.mkdir(parents=True, exist_ok=True)
        copy.write_bytes(path.read_bytes())


def _fill(folder: Path, project: Project, editor: str) -> tuple[str, ...]:
    """Write the files of the extension of one editor to an empty folder.

    Args:
        folder: The folder.
        project: The project.
        editor: `zed` or `code`.

    Returns:
        The hints.

    Raises:
        KitError: `code` and the program has no `.vsix`.
    """
    built = vsix()
    match editor, built:
        case "zed", _:
            names, hints = zed_languages(tuple(sorted(project.config.code_suffixes)))
            _copy_plain(ZED_SOURCE, folder)
            template = (ZED_SOURCE / "extension.toml").read_text(encoding="utf-8")
            listed = ", ".join(json.dumps(n) for n in names)
            (folder / "extension.toml").write_text(
                template.replace("{languages}", listed), encoding="utf-8"
            )
        case "code", Path():
            shutil.copyfile(built, folder / VSIX)
            hints = ()
        case "code", None:
            raise KitError(
                "this program has no VS Code extension; run specs from the flake of the kit"
            )
        case _:
            raise KitError(f"unknown editor {editor!r}; use zed or code")
    (folder / "server.json").write_text(server_json(project), encoding="utf-8")
    return hints


def _git(project: Project, *args: str) -> subprocess.CompletedProcess[str]:
    """Run git in the project.

    Args:
        project: The project.
        *args: The arguments.

    Returns:
        The result.
    """
    return subprocess.run(
        ("git", *args), cwd=project.root, capture_output=True, text=True, check=False
    )


def ignore(project: Project, rel: str) -> None:
    """Add a folder to `.gitignore`, except when git tracks a file of it or ignores it already.

    Args:
        project: The project.
        rel: The folder from the root of the project.
    """
    tracked = _git(project, "ls-files", "--", rel).stdout.strip() != ""
    ignored = _git(project, "check-ignore", "-q", f"{rel}/").returncode == 0
    path = project.root / ".gitignore"
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    if not tracked and not ignored:
        write_text(path, f"{text}{'' if text.endswith('\n') or not text else '\n'}/{rel}/\n")


def write(project: Project, editor: str) -> tuple[str, ...]:
    """Write the whole folder of the extension of one editor again, and keep it out of git.

    Args:
        project: The project.
        editor: `zed` or `code`.

    Returns:
        The hints.
    """
    rel = FOLDERS.get(editor, "")
    with tempfile.TemporaryDirectory() as tmp:
        hints = _fill(Path(tmp), project, editor)
        replace_tree_all(Path(tmp), project.root / rel)
    ignore(project, rel)
    return hints


def refresh(project: Project) -> tuple[str, ...]:
    """Write each folder of an extension again that is in the project (§000067).

    Args:
        project: The project.

    Returns:
        The hints. A folder of VS Code stays when the program has no `.vsix`.
    """
    present = tuple(e for e, rel in FOLDERS.items() if (project.root / rel).is_dir())
    return tuple(
        hint
        for editor in present
        for hint in (
            write(project, editor)
            if editor != "code" or vsix()
            else (f"{FOLDERS[editor]}/ stays: this program has no VS Code extension",)
        )
    )


def setup(project: Project, editor: str, ask: Ask) -> tuple[str, tuple[str, ...]]:
    """Write the folder of the extension, then install it in VS Code after a yes (§000089).

    Args:
        project: The project.
        editor: `zed` or `code`.
        ask: The questions.

    Returns:
        The message and the hints.
    """
    hints = write(project, editor)
    path = project.root / FOLDERS["code"] / VSIX
    run = (
        editor == "code"
        and ask.interactive
        and ask.confirm(f"Run code --install-extension {FOLDERS['code']}/{VSIX}?", True)
    )
    done = (
        run
        and subprocess.run(("code", "--install-extension", str(path)), check=False).returncode == 0
    )
    return f"wrote {FOLDERS[editor]}/", (
        *hints,
        "installed the extension in VS Code" if done else install_hint(editor),
    )


def install_hint(editor: str) -> str:
    """Return how to install the extension in the editor.

    Args:
        editor: `zed` or `code`.

    Returns:
        The hint.
    """
    match editor:
        case "zed":
            return (
                "in Zed, run the action `zed: install dev extension` and choose .zed/specs/;"
                " Zed needs rustup to build the extension"
            )
        case _:
            return f"install the extension: code --install-extension {FOLDERS['code']}/{VSIX}"
