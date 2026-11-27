"""Tests of `specs install` (§000083) and of `specs.lock` (§000082)."""

from __future__ import annotations

import shutil
from pathlib import Path

from conftest import Kit

COPY = "specs/.upstream/github.com/frederikbeimgraben/specs"
RULE = f"{COPY}/workflow/specs/process/000001_precedence.md"


def _changes(out: str) -> list[str]:
    """Return the lines of the changed files.

    Args:
        out: The output of the command.

    Returns:
        The lines that start with a mark.
    """
    return [line for line in out.splitlines() if line[:2] in {"A ", "M ", "D "}]


def test_install_changes_nothing_on_a_current_project(kit: Kit, project: Path) -> None:
    """`specs install` on a current project changes no file and finds no error."""
    result = kit.run(project, "install", "--raw")
    assert result.code == 0, result.out + result.err
    assert not _changes(result.out)


def test_install_restores_a_changed_copy(kit: Kit, project: Path) -> None:
    """The check finds a changed copy, and `specs install` loads the copy again."""
    path = project / RULE
    before = path.read_text(encoding="utf-8")
    path.write_text(before + "More text.\n", encoding="utf-8")
    checked = kit.run(project, "check", "--raw")
    assert checked.code == 1
    assert "does not agree with its hash in specs.lock" in checked.out
    result = kit.run(project, "install", "--raw")
    assert result.code == 0, result.out + result.err
    assert f"M {RULE}" in result.out
    assert path.read_text(encoding="utf-8") == before


def test_install_loads_a_missing_copy(kit: Kit, project: Path) -> None:
    """`specs install` loads a copy that does not exist at the commit of `specs.lock`."""
    shutil.rmtree(project / "specs/.upstream")
    result = kit.run(project, "install", "--raw")
    assert result.code == 0, result.out + result.err
    assert (project / RULE).is_file()


def test_install_writes_missing_kit_files(kit: Kit, project: Path) -> None:
    """`specs install` writes a missing template, CI file and `CLAUDE.md`."""
    for name in ("specs/.templates/TEMPLATE.md", ".github/workflows/specs.yml", "CLAUDE.md"):
        (project / name).unlink()
    result = kit.run(project, "install", "--raw")
    assert result.code == 0, result.out + result.err
    for name in ("specs/.templates/TEMPLATE.md", ".github/workflows/specs.yml", "CLAUDE.md"):
        assert f"A {name}" in result.out


def test_install_keeps_a_changed_template(kit: Kit, project: Path) -> None:
    """`specs install` keeps a template that is not the same as in the kit."""
    path = project / "specs/.templates/TEMPLATE.md"
    path.write_text("my template\n", encoding="utf-8")
    result = kit.run(project, "install", "--raw")
    assert result.code == 0, result.out + result.err
    assert path.read_text(encoding="utf-8") == "my template\n"
