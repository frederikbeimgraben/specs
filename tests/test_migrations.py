"""Tests of the migrations (§000081)."""

from __future__ import annotations

import json
import shutil
import stat
from importlib import resources
from pathlib import Path

from conftest import RULES_REPO, Kit, git, write_rule

from spezi.agents import BEGIN, END
from spezi.changes import move_tree
from spezi.migrations import m0005_spezi_name

NEW_KIT = "github.com/frederikbeimgraben/spezi"
OLD_KIT = "github.com/frederikbeimgraben/specs"


def _old_layout(project: Path) -> None:
    """Move the files of the kit back to the layout and the names before migration 1.

    Args:
        project: The root of the project.
    """
    old = project / ".specs"
    old.mkdir()
    shutil.move(project / "specs" / ".upstream", old / "upstream")
    shutil.move(project / "specs" / ".templates", old / "templates")
    shutil.copy(project / "specs" / "README.md", old / "index.md")
    shutil.move(old / "upstream" / NEW_KIT, old / "upstream" / OLD_KIT)
    config = (project / "spezi.toml").read_text(encoding="utf-8")
    (project / "specs.toml").write_text(config.replace(NEW_KIT, OLD_KIT), encoding="utf-8")
    (project / "spezi.toml").unlink()
    (project / "spezi.lock").unlink()


def test_update_moves_the_old_layout(kit: Kit, project: Path) -> None:
    """`specs update` moves `.specs/` below `specs/` and lists the moved files."""
    _old_layout(project)
    result = kit.run(project, "update", "kit", kit.rev, "--raw")
    assert result.code == 0, result.out + result.err
    assert not (project / ".specs").exists()
    assert (project / "specs/.templates/TEMPLATE.md").is_file()
    assert (
        project / "specs/.upstream/github.com/frederikbeimgraben/spezi/workflow/specs/process"
    ).is_dir()
    assert "migrated: move .specs/ below specs/" in result.out
    assert "D .specs/index.md" in result.out


def test_a_read_only_folder_moves_and_stays_writable(tmp_path: Path) -> None:
    """An old program copied the kit with the read-only modes of the Nix store.

    Only the copy is read-only, not the folder that holds it. The move must delete the copy and
    give a new copy that can change.
    """
    old = tmp_path / ".specs" / "templates"
    old.mkdir(parents=True)
    (old / "TEMPLATE.md").write_text("template\n", encoding="utf-8")
    for path in (old / "TEMPLATE.md", old):
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
        assert "run spezi update first" in result.err
        assert RULES_REPO not in (project / "spezi.toml").read_text(encoding="utf-8")
    finally:
        git(kit.rules, "reset", "-q", "--hard", kit.rules_rev, env=kit.env)


def _old_names(root: Path) -> None:
    """Write the files of a project with the names before migration 5.

    Args:
        root: The root of the project.
    """
    kit_copy = root / "specs" / ".upstream" / OLD_KIT / "workflow"
    kit_copy.mkdir(parents=True)
    (kit_copy / "rule.md").write_text("see github.com/frederikbeimgraben/specs:000001\n")
    (root / "specs.toml").write_text(f'forge = "github"\n\n[upstream."{OLD_KIT}"]\nref = "v1"\n')
    (root / "specs.lock").write_text(f'[upstream."{OLD_KIT}"]\nref = "v1"\n')
    for name in ("spec-write", "spec-check"):
        (root / ".claude" / "skills" / name).mkdir(parents=True)
        (root / ".claude" / "skills" / name / "SKILL.md").write_text(f"{name}\n")
    (root / ".zed" / "specs").mkdir(parents=True)
    (root / ".gitignore").write_text("/.zed/specs/\nbuild/\n")
    template = (resources.files("spezi") / "data" / "github-workflow.yml").read_text()
    workflow = root / ".github" / "workflows" / "specs.yml"
    workflow.parent.mkdir(parents=True)
    workflow.write_text(
        template.replace("spezi", "specs").replace("{ref}", "a" * 40).replace("{branch}", "main")
    )
    (root / ".mcp.json").write_text('{"mcpServers": {"other": {}, "specs": {"command": "nix"}}}')
    (root / "AGENTS.md").write_text(
        "# Mine\n\n<!-- specs:begin (written by specs install, do not edit) -->\nrules\n"
        "<!-- specs:end -->\n"
    )
    rule = root / "specs" / "workflow" / "a" / "b" / "000100_x.md"
    rule.parent.mkdir(parents=True)
    rule.write_text(
        "implementation:\n  - specs.toml\n  - .claude/skills/spec-write/SKILL.md\n"
        "see github.com/frederikbeimgraben/specs:W/specs/process/000001, specs.toml.bak\n"
    )


def test_migration_5_gives_the_files_the_new_name(tmp_path: Path) -> None:
    """Migration 5 renames each file of the kit, and a second run changes nothing."""
    _old_names(tmp_path)
    m0005_spezi_name.project(tmp_path)
    before = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    m0005_spezi_name.project(tmp_path)
    after = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    assert after == before
    assert not (tmp_path / "specs.toml").exists() and not (tmp_path / "specs.lock").exists()
    assert f'[upstream."{NEW_KIT}"]' in (tmp_path / "spezi.toml").read_text()
    assert f'[upstream."{NEW_KIT}"]' in (tmp_path / "spezi.lock").read_text()
    assert (tmp_path / "specs" / ".upstream" / NEW_KIT / "workflow" / "rule.md").is_file()
    assert sorted(p.name for p in (tmp_path / ".claude" / "skills").iterdir()) == [
        "spezi-check",
        "spezi-write",
    ]
    assert (tmp_path / ".zed" / "spezi").is_dir() and not (tmp_path / ".zed" / "specs").exists()
    assert (tmp_path / ".gitignore").read_text() == "/.zed/spezi/\nbuild/\n"
    workflow = (tmp_path / ".github" / "workflows" / "spezi.yml").read_text()
    assert "name: spezi" in workflow and "github:frederikbeimgraben/spezi/" + "a" * 40 in workflow
    assert not (tmp_path / ".github" / "workflows" / "specs.yml").exists()
    assert list(json.loads((tmp_path / ".mcp.json").read_text())["mcpServers"]) == [
        "other",
        "spezi",
    ]
    assert (tmp_path / "AGENTS.md").read_text() == f"# Mine\n\n{BEGIN}\nrules\n{END}\n"
    rule = tmp_path / "specs" / "workflow" / "a" / "b" / "000100_x.md"
    assert rule.read_text() == (
        "implementation:\n  - spezi.toml\n  - .claude/skills/spezi-write/SKILL.md\n"
        f"see {NEW_KIT}:W/specs/process/000001, specs.toml.bak\n"
    )


def test_migration_5_keeps_a_changed_ci_file(tmp_path: Path) -> None:
    """Migration 5 does not move a CI file that a person changed."""
    workflow = tmp_path / ".github" / "workflows" / "specs.yml"
    workflow.parent.mkdir(parents=True)
    workflow.write_text("name: specs\njobs: {}\n")
    m0005_spezi_name.project(tmp_path)
    assert workflow.read_text() == "name: specs\njobs: {}\n"
    assert not (tmp_path / ".github" / "workflows" / "spezi.yml").exists()


def test_migration_5_renames_the_kit_in_a_copy(tmp_path: Path) -> None:
    """Migration 5 gives the long IDs of the kit in a copy the new name."""
    rule = tmp_path / "style" / "000001_x.md"
    rule.parent.mkdir(parents=True)
    rule.write_text(f"see {OLD_KIT}:000002 and notgithub.com/frederikbeimgraben/specs:x\n")
    m0005_spezi_name.copy(tmp_path)
    assert rule.read_text() == (
        f"see {NEW_KIT}:000002 and notgithub.com/frederikbeimgraben/specs:x\n"
    )


def test_migration_5_renames_the_flake_input(tmp_path: Path) -> None:
    """Migration 5 renames the input of a `flake.nix` of the kit and its node in `flake.lock`."""
    template = (resources.files("spezi") / "data" / "flake.nix").read_text()
    (tmp_path / "flake.nix").write_text(
        template.replace("spezi", "specs").replace("{ref}", "b" * 40)
    )
    node = {"locked": {"owner": "frederikbeimgraben", "repo": "specs", "rev": "b" * 40}}
    lock = {
        "nodes": {"root": {"inputs": {"nixpkgs": "nixpkgs", "specs": "specs"}}, "specs": node},
        "root": "root",
        "version": 7,
    }
    (tmp_path / "flake.lock").write_text(json.dumps(lock))
    m0005_spezi_name.project(tmp_path)
    assert (tmp_path / "flake.nix").read_text() == template.replace("{ref}", "b" * 40)
    nodes = json.loads((tmp_path / "flake.lock").read_text())["nodes"]
    assert nodes["root"]["inputs"] == {"nixpkgs": "nixpkgs", "spezi": "spezi"}
    assert nodes["spezi"]["locked"]["repo"] == "spezi" and "specs" not in nodes
