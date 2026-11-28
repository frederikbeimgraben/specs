"""Tests of the questions of `specs init`, `specs add` and `specs update` (§000085)."""

from __future__ import annotations

import tomllib
from pathlib import Path

import pytest
from conftest import RULES_REPO, Kit, git, write_rule
from script import PROPOSAL, Script, inside

from spezi.ask import Cancelled
from spezi.kit import add, init, update
from spezi.project import Project


def _config(root: Path) -> dict[str, object]:
    """Return the parsed `spezi.toml`.

    Args:
        root: The root of the project.

    Returns:
        The settings.
    """
    return tomllib.loads((root / "spezi.toml").read_text(encoding="utf-8"))


def _code(root: Path, kit: Kit) -> None:
    """Add a tracked Python file in `src/` and a tracked text file in `docs/`.

    Args:
        root: The root of the project.
        kit: The kit.
    """
    (root / "src").mkdir()
    (root / "src/app.py").write_text("x = 1\n", encoding="utf-8")
    (root / "docs").mkdir()
    (root / "docs/notes.txt").write_text("notes\n", encoding="utf-8")
    git(root, "add", "-A", env=kit.env)


def test_init_takes_the_proposals_without_a_terminal(kit: Kit, empty: Path) -> None:
    """Without a terminal, init takes the proposals: the folders with code are code_dirs."""
    _code(empty, kit)
    result = kit.run(empty, "init", "--forge", "github", "--raw")
    assert result.code == 0, result.out + result.err
    config = _config(empty)
    assert config["code_dirs"] == ["src"]
    assert config["base_ref"] == "origin/main"
    assert config["features"] == dict.fromkeys(
        ("mcp", "agents", "claude", "ci", "skills", "flake", "envrc"), True
    )


def test_init_writes_the_answers(kit: Kit, empty: Path) -> None:
    """Init writes the answers to spezi.toml and the login to git config --local."""
    _code(empty, kit)
    script = Script(
        [
            "gitlab",
            "origin/develop",
            ("src", "docs"),
            (".py", ".txt"),
            "example.com/group/project",
            (),
            "someone",
            ("agents", "ci", "flake"),
            True,
        ]
    )
    with inside(kit.env, empty):
        init(empty, None, script)
    config = _config(empty)
    assert config["forge"] == "gitlab"
    assert config["base_ref"] == "origin/develop"
    assert config["code_dirs"] == ["src", "docs"]
    assert config["code_suffixes"] == [".py", ".txt"]
    assert config["repo"] == "example.com/group/project"
    assert config["features"]["mcp"] is False  # type: ignore[index]
    assert config["features"]["ci"] is True  # type: ignore[index]
    assert git(empty, "config", "--local", "gitlab.user", env=kit.env).strip() == "someone"
    assert not (empty / ".mcp.json").exists()
    assert "# The base branch." in (empty / "spezi.toml").read_text(encoding="utf-8")


def test_init_cancel_changes_no_file(kit: Kit, empty: Path) -> None:
    """An answer no to Run? stops init before it changes a file."""
    script = Script(["github", PROPOSAL, PROPOSAL, PROPOSAL, "", PROPOSAL, False])
    with inside(kit.env, empty), pytest.raises(Cancelled):
        init(empty, None, script)
    assert not (empty / "spezi.toml").exists()


def test_add_asks_for_the_folders(kit: Kit, project: Path) -> None:
    """Add asks for the repository, the ref and the folders, and writes include."""
    script = Script([RULES_REPO, "main", ("agents", "agents/work"), True])
    with inside(kit.env, project):
        add(Project.open(project), None, None, (), script)
    table = _config(project)["upstream"][RULES_REPO]  # type: ignore[index]
    assert table == {"ref": "main", "include": ["agents/"]}
    assert any("A 000002 An agent runs the tests" in s for s in script.shown)
    assert not (project / "specs/.upstream" / RULES_REPO / "style").exists()


def test_update_keeps_a_changed_template(kit: Kit, project: Path) -> None:
    """Update shows the diff of a changed template, and keep keeps the file."""
    path = project / "specs/.templates/TEMPLATE.md"
    path.write_text("my template\n", encoding="utf-8")
    script = Script([(), "keep", True])
    with inside(kit.env, project):
        update(Project.open(project), "kit", None, script)
    assert path.read_text(encoding="utf-8") == "my template\n"
    assert any("my template" in s for s in script.shown)


def test_update_stops_for_a_changed_template_without_a_terminal(kit: Kit, project: Path) -> None:
    """Without a terminal, update stops for a changed template and keeps it."""
    path = project / "specs/.templates/TEMPLATE.md"
    path.write_text("my template\n", encoding="utf-8")
    result = kit.run(project, "update", "kit", "--raw")
    assert result.code == 1
    assert "specs/.templates/TEMPLATE.md" in result.err
    assert path.read_text(encoding="utf-8") == "my template\n"


def test_update_stops_for_a_removed_rule_without_a_terminal(kit: Kit, project: Path) -> None:
    """Without a terminal, update stops when the new version removes a rule that a rule names."""
    assert kit.run(project, "add", RULES_REPO, "main").code == 0
    write_rule(
        project,
        "decisions/work/naming",
        "000001",
        "use-names",
        "The project uses the names rule",
        "decision",
        f"The project must follow {RULES_REPO}:000001.",
    )
    (kit.rules / "specs/style/python/naming/000001_snake-case.md").unlink()
    kit.commit_rules()
    try:
        result = kit.run(project, "update", RULES_REPO, "--raw")
        assert result.code == 1
        assert "replaces or removes rules" in result.err
        assert (project / "specs/.upstream" / RULES_REPO / "style").is_dir()
    finally:
        git(kit.rules, "reset", "-q", "--hard", kit.rules_rev, env=kit.env)
