"""Tests of the migrations (§000081)."""

from __future__ import annotations

import shutil
from pathlib import Path

from conftest import RULES_REPO, Kit, git


def _old_layout(project: Path) -> None:
    """Move the files of the kit back to the layout before migration 1.

    Args:
        project: The root of the project.
    """
    old = project / ".specs"
    old.mkdir()
    shutil.move(project / "specs" / ".upstream", old / "upstream")
    shutil.move(project / "specs" / ".templates", old / "templates")
    shutil.copy(project / "specs" / "README.md", old / "index.md")
    (project / "specs.lock").unlink()


def test_update_moves_the_old_layout(kit: Kit, project: Path) -> None:
    """`specs update` moves `.specs/` below `specs/` and lists the moved files."""
    _old_layout(project)
    result = kit.run(project, "update", "kit", kit.rev, "--raw")
    assert result.code == 0, result.out + result.err
    assert not (project / ".specs").exists()
    assert (project / "specs/.templates/TEMPLATE.md").is_file()
    assert (
        project / "specs/.upstream/github.com/frederikbeimgraben/specs/workflow/specs/process"
    ).is_dir()
    assert "migrated: move .specs/ below specs/" in result.out
    assert "D .specs/index.md" in result.out


def test_a_migration_changes_nothing_twice(kit: Kit, project: Path) -> None:
    """A project in the new layout stays as it is."""
    result = kit.run(project, "update", "kit", kit.rev, "--raw")
    assert result.code == 0, result.out + result.err
    assert not [line for line in result.out.splitlines() if line.startswith(("A ", "D "))]


def test_add_stops_for_a_newer_kit(kit: Kit, project: Path) -> None:
    """`specs add` stops when the repository needs a newer kit than the project."""
    (kit.rules / "specs.toml").write_text(
        '[upstream."github.com/frederikbeimgraben/specs"]\nref = "' + "f" * 40 + '"\n',
        encoding="utf-8",
    )
    rev = kit.commit_rules()
    try:
        result = kit.run(project, "add", RULES_REPO, rev, "--raw")
        assert result.code == 1
        assert "run specs update first" in result.err
        assert RULES_REPO not in (project / "specs.toml").read_text(encoding="utf-8")
    finally:
        git(kit.rules, "reset", "-q", "--hard", kit.rules_rev, env=kit.env)
