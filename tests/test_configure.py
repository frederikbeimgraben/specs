"""Tests of `specs configure` and `specs remove` (spec 000086, 000087)."""

from __future__ import annotations

import tomllib
from pathlib import Path

import pytest
from conftest import RULES_REPO, Kit
from script import Script, inside

from spezi.ask import Cancelled
from spezi.configure import configure
from spezi.project import Project


def _config(root: Path) -> dict[str, object]:
    """Return the parsed `spezi.toml`.

    Args:
        root: The root of the project.

    Returns:
        The settings.
    """
    return tomllib.loads((root / "spezi.toml").read_text(encoding="utf-8"))


def test_configure_sets_a_switch(kit: Kit, project: Path) -> None:
    """Configure with a key and a value sets the switch and runs install."""
    result = kit.run(project, "configure", "features.mcp", "false", "--raw")
    assert result.code == 0, result.out + result.err
    assert _config(project)["features"]["mcp"] is False  # type: ignore[index]
    assert not (project / ".mcp.json").exists()
    assert "D .mcp.json" in result.out


def test_configure_keeps_the_comments(kit: Kit, project: Path) -> None:
    """Configure changes only the value and keeps the comments of spezi.toml."""
    before = (project / "spezi.toml").read_text(encoding="utf-8")
    assert kit.run(project, "configure", "code_dirs", "src,lib").code == 0
    after = (project / "spezi.toml").read_text(encoding="utf-8")
    assert after == before.replace("code_dirs = []", 'code_dirs = ["src", "lib"]')


def test_configure_stops_for_a_bad_value(kit: Kit, project: Path) -> None:
    """Configure stops with an error for a value of a different form."""
    before = (project / "spezi.toml").read_text(encoding="utf-8")
    result = kit.run(project, "configure", "max_elements", "zero", "--raw")
    assert result.code == 1
    assert "whole number" in result.err
    assert (project / "spezi.toml").read_text(encoding="utf-8") == before


def test_configure_stops_for_claude_without_agents(kit: Kit, project: Path) -> None:
    """Configure stops when the settings break the rule of claude and agents."""
    result = kit.run(project, "configure", "features.agents", "false", "--raw")
    assert result.code == 1
    assert "features.claude needs features.agents" in result.err


def test_configure_needs_a_terminal_or_a_key(kit: Kit, project: Path) -> None:
    """Without a terminal, configure without a key stops with an error."""
    result = kit.run(project, "configure", "--raw")
    assert result.code == 1
    assert "needs a terminal" in result.err


def test_the_menu_saves_the_changes(kit: Kit, project: Path) -> None:
    """The menu changes the values in memory, and save writes them."""
    script = Script(["features.mcp = true", "max_elements = 25", "40", "save"])
    with inside(kit.env, project):
        assert configure(Project.open(project), script)
    config = _config(project)
    assert config["max_elements"] == 40
    assert config["features"]["mcp"] is False  # type: ignore[index]


def test_the_menu_discards_the_changes(kit: Kit, project: Path) -> None:
    """Discard asks once and changes no file."""
    before = (project / "spezi.toml").read_text(encoding="utf-8")
    script = Script(["features.ci = true", "discard", True])
    with inside(kit.env, project), pytest.raises(Cancelled):
        configure(Project.open(project), script)
    assert (project / "spezi.toml").read_text(encoding="utf-8") == before


def test_remove_deletes_the_copy(kit: Kit, project: Path) -> None:
    """Remove deletes the table, the copy and the entry in spezi.lock."""
    assert kit.run(project, "add", RULES_REPO, "main").code == 0
    result = kit.run(project, "remove", RULES_REPO, "--raw")
    assert result.code == 0, result.out + result.err
    assert RULES_REPO not in _config(project)["upstream"]  # type: ignore[operator]
    assert not (project / "specs/.upstream/example.com").exists()
    assert RULES_REPO not in (project / "spezi.lock").read_text(encoding="utf-8")


def test_remove_stops_for_the_kit(kit: Kit, project: Path) -> None:
    """Remove stops with an error for the kit."""
    result = kit.run(project, "remove", "kit", "--raw")
    assert result.code == 1
    assert "the kit cannot be removed" in result.err
