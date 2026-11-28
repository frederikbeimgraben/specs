"""Tests of `specs setup-ide` (§000089)."""

from __future__ import annotations

import json
import stat
import subprocess
import sys
from pathlib import Path

import pytest
from conftest import Kit, Result, git

from spezi import ide
from spezi.project import Project


def _run(kit: Kit, project: Path, *args: str, vsix: Path | None = None) -> Result:
    """Run the command, with `SPEZI_VSIX` when a `.vsix` is given.

    Args:
        kit: The kit.
        project: The root of the project.
        *args: The arguments.
        vsix: The `.vsix`, or None.

    Returns:
        The result.
    """
    done = subprocess.run(
        (sys.executable, "-m", "spezi", *args),
        cwd=project,
        env={**kit.env, **({"SPEZI_VSIX": str(vsix)} if vsix else {})},
        capture_output=True,
        text=True,
        check=False,
    )
    return Result(done.returncode, done.stdout, done.stderr)


def test_zed_gets_the_source_of_the_extension(kit: Kit, project: Path) -> None:
    """The Zed folder holds the source with the languages of the suffixes and `server.json`."""
    result = _run(kit, project, "setup-ide", "zed", "--raw")
    folder = project / ".zed" / "spezi"
    manifest = (folder / "extension.toml").read_text(encoding="utf-8")
    server = json.loads((folder / "server.json").read_text(encoding="utf-8"))
    assert result.code == 0, result.out + result.err
    assert 'languages = ["Markdown", "Go", "Java", "JavaScript", "Kotlin", "Nix", "Python",' in (
        manifest
    )
    assert (folder / "src" / "lib.rs").is_file()
    assert (folder / "Cargo.toml").is_file()
    assert server["suffixes"] == [".go", ".java", ".js", ".kt", ".nix", ".py", ".rs", ".sh", ".ts"]
    assert server["command"]
    assert "zed: install dev extension" in result.out
    assert "A .zed/spezi/server.json" in result.out


def test_code_gets_the_vsix(kit: Kit, project: Path, tmp_path: Path) -> None:
    """The VS Code folder holds the `.vsix`; with `-y` the command only shows how to install."""
    missing = _run(kit, project, "setup-ide", "code", "--raw")
    assert missing.code == 1
    assert not (project / ".vscode" / "spezi").exists()
    vsix = tmp_path / "spezi.vsix"
    vsix.write_bytes(b"vsix")
    result = _run(kit, project, "setup-ide", "code", "-y", "--raw", vsix=vsix)
    assert result.code == 0, result.out + result.err
    assert (project / ".vscode" / "spezi" / "spezi.vsix").read_bytes() == b"vsix"
    assert "code --install-extension .vscode/spezi/spezi.vsix" in result.out


def test_the_folder_goes_to_gitignore(kit: Kit, project: Path) -> None:
    """The command adds the folder to `.gitignore` once."""
    assert _run(kit, project, "setup-ide", "zed", "--raw").code == 0
    assert _run(kit, project, "setup-ide", "zed", "--raw").code == 0
    lines = (project / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert lines.count("/.zed/spezi/") == 1


def test_a_tracked_folder_stays_out_of_gitignore(kit: Kit, project: Path) -> None:
    """A folder with a tracked file does not go to `.gitignore`."""
    tracked = project / ".zed" / "spezi" / "notes.txt"
    tracked.parent.mkdir(parents=True)
    tracked.write_text("notes\n", encoding="utf-8")
    git(project, "add", str(tracked), env=kit.env)
    assert _run(kit, project, "setup-ide", "zed", "--raw").code == 0
    gitignore = project / ".gitignore"
    text = gitignore.read_text(encoding="utf-8") if gitignore.is_file() else ""
    assert "/.zed/spezi/" not in text


def test_update_writes_the_folder_again(kit: Kit, project: Path) -> None:
    """`specs update` of the kit writes a folder of an extension again."""
    assert _run(kit, project, "setup-ide", "zed", "--raw").code == 0
    server = project / ".zed" / "spezi" / "server.json"
    before = server.read_text(encoding="utf-8")
    server.write_text("{}\n", encoding="utf-8")
    result = kit.run(project, "update", "kit", kit.rev, "--raw")
    assert result.code == 0, result.out + result.err
    assert server.read_text(encoding="utf-8") == before


def test_a_read_only_source_gives_files_that_can_change(
    project: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A source in the Nix store is read-only; the folder in the project must stay writable."""
    source = tmp_path / "store"
    for path in sorted(p for p in ide.ZED_SOURCE.rglob("*") if p.is_file()):
        copy = source / path.relative_to(ide.ZED_SOURCE)
        copy.parent.mkdir(parents=True, exist_ok=True)
        copy.write_bytes(path.read_bytes())
    for path in sorted(source.rglob("*"), reverse=True):
        path.chmod(0o555 if path.is_dir() else 0o444)
    source.chmod(0o555)
    monkeypatch.setattr(ide, "ZED_SOURCE", source)
    monkeypatch.chdir(project)
    try:
        ide.write(Project.open(project), "zed")
    finally:
        for path in (source, *source.rglob("*")):
            path.chmod(0o755)
    folder = project / ".zed" / "spezi"
    assert '"Markdown"' in (folder / "extension.toml").read_text(encoding="utf-8")
    assert all(p.stat().st_mode & stat.S_IWUSR for p in (folder, *folder.rglob("*")))
