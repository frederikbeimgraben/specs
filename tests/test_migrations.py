"""Tests of the migrations (§000081)."""

from __future__ import annotations

import shutil
import stat
from pathlib import Path

from conftest import RULES_REPO, Kit, git, write_rule

from specs_kit.changes import move_tree


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


def test_a_read_only_folder_moves_and_stays_writable(tmp_path: Path) -> None:
    """An old program copied the kit with the read-only modes of the Nix store.

    The move must delete the old folder and give a copy that can change.
    """
    old = tmp_path / ".specs" / "templates"
    old.mkdir(parents=True)
    (old / "TEMPLATE.md").write_text("template\n", encoding="utf-8")
    for path in (old / "TEMPLATE.md", old, old.parent):
        path.chmod(0o444 if path.is_file() else 0o555)
    new = tmp_path / "specs" / ".templates"
    try:
        move_tree(old, new)
    finally:
        for path in (old.parent, *old.parent.rglob("*")) if old.parent.exists() else ():
            path.chmod(0o755)
    assert not old.exists()
    assert (new / "TEMPLATE.md").read_text(encoding="utf-8") == "template\n"
    assert all(p.stat().st_mode & stat.S_IWUSR for p in (new, *new.rglob("*")))


def test_update_changes_the_old_paths_in_the_specs(kit: Kit, project: Path) -> None:
    """`specs update` changes a path below `.specs/` in a spec of the project to its new place."""
    (project / "src").mkdir(exist_ok=True)
    rule = write_rule(
        project,
        "conventions/specs/format",
        "000100",
        "templates",
        "Rule 000100",
        "convention",
        "A spec must copy `.specs/templates/TEMPLATE.md`, see `.specs/index.md` and"
        " `.specs/upstream/`.",
    )
    _old_layout(project)
    result = kit.run(project, "update", "kit", kit.rev, "--raw")
    text = rule.read_text(encoding="utf-8")
    assert result.code == 0, result.out + result.err
    assert (
        "copy `specs/.templates/TEMPLATE.md`, see `specs/README.md` and `specs/.upstream/`" in text
    )
    assert ".specs/" not in text
    assert "migrated: change the paths below .specs/ in the specs of the project" in result.out
    assert "M specs/conventions/specs/format/000100_templates.md" in result.out


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
