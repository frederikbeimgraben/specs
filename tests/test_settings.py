"""Tests of `spezi.toml` (§000078) and of the block in `AGENTS.md` (§000079)."""

from __future__ import annotations

from pathlib import Path

import pytest
from conftest import RULES_REPO, Kit

BEGIN = "<!-- spezi:begin (written by spezi install, do not edit) -->"


@pytest.mark.parametrize(
    ("old", "new", "message"),
    [
        ("code_dirs = []", 'code_dirs = "src"', "code_dirs"),
        ("max_elements = 25", "max_elements = 0", "max_elements"),
        ('forge = "github"', "forge = [", "spezi.toml"),
        ('forge = "github"', 'forge = "gitea"', "forge must be github, gitlab, codeberg"),
        ("code_dirs = []", "code_dir = []", "unknown key code_dir"),
    ],
)
def test_a_bad_setting_stops_each_command(
    kit: Kit, project: Path, old: str, new: str, message: str
) -> None:
    """A wrong type or forge, an unknown key or no valid TOML stops the command with code 1."""
    path = project / "spezi.toml"
    text = path.read_text(encoding="utf-8")
    assert old in text
    path.write_text(text.replace(old, new), encoding="utf-8")
    for args in (("check", "--raw"), ("list", "--raw")):
        result = kit.run(project, *args)
        assert result.code == 1
        assert result.err.startswith("spezi: spezi.toml: ")
        assert message in result.err
        assert result.err.count("\n") == 1


def test_init_writes_the_settings_without_comments(kit: Kit, project: Path) -> None:
    """`spezi init` writes `spezi.toml` with each key and its default, and with no comment."""
    text = (project / "spezi.toml").read_text(encoding="utf-8")
    assert "#" not in text
    assert 'base_ref = "origin/main"' in text
    assert "max_elements = 25" in text
    assert "envrc = true" in text


def test_init_writes_agents_and_claude(kit: Kit, project: Path) -> None:
    """`specs init` creates `CLAUDE.md` with the import and lists the approved A and W rules."""
    agents = (project / "AGENTS.md").read_text(encoding="utf-8")
    assert (project / "CLAUDE.md").read_text(encoding="utf-8") == "@AGENTS.md\n"
    assert agents.startswith(BEGIN)
    assert "spezi:A/work/questions/000043" in agents
    assert "spezi:W/specs/process/000001" in agents
    assert ":S/" not in agents and ":F/" not in agents


def test_init_keeps_an_existing_claude(kit: Kit, empty: Path) -> None:
    """`specs init` keeps a `CLAUDE.md` without the import and prints the line to add."""
    (empty / "CLAUDE.md").write_text("# Mine\n", encoding="utf-8")
    result = kit.run(empty, "init", "--forge", "github", "--raw")
    assert (empty / "CLAUDE.md").read_text(encoding="utf-8") == "# Mine\n"
    assert "add the line @AGENTS.md to CLAUDE.md" in result.out


def test_the_block_keeps_the_text_around_it(kit: Kit, project: Path) -> None:
    """`specs install` replaces only the block and keeps the text before and after it."""
    path = project / "AGENTS.md"
    path.write_text(f"# Head\n\n{path.read_text(encoding='utf-8')}\n# Tail\n", encoding="utf-8")
    assert kit.run(project, "add", RULES_REPO, kit.rules_rev).code == 0
    text = path.read_text(encoding="utf-8")
    assert text.startswith("# Head\n\n" + BEGIN)
    assert text.endswith("\n# Tail\n")
    assert "example.com/team/rules:A/work/tests/000002" in text


def test_a_file_without_block_gets_it_at_the_end(kit: Kit, project: Path) -> None:
    """`specs install` adds the block at the end of a file without it."""
    path = project / "AGENTS.md"
    path.write_text("# Mine\n", encoding="utf-8")
    assert kit.run(project, "check", "--raw").code == 1
    assert kit.run(project, "install", "--raw").code == 0
    assert path.read_text(encoding="utf-8").startswith(f"# Mine\n\n{BEGIN}")


def test_an_unknown_key_of_a_copy_stops_each_command(kit: Kit, project: Path) -> None:
    """An unknown key in a table `[upstream."<repo>"]` stops the command with one line."""
    path = project / "spezi.toml"
    path.write_text(
        path.read_text(encoding="utf-8").replace('\nref = "', '\nrev = "x"\nref = "', 1),
        encoding="utf-8",
    )
    result = kit.run(project, "check", "--raw")
    assert result.code == 1
    assert result.err.startswith("spezi: spezi.toml: unknown key rev in [upstream.")
