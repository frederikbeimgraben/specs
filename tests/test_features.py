"""Tests of the switches in `[features]` of `specs.toml` (§000084)."""

from __future__ import annotations

from pathlib import Path

from conftest import Kit


def _switch(project: Path, **switches: bool) -> None:
    """Set switches of `[features]` in `specs.toml`.

    Args:
        project: The root of the project.
        **switches: The new value of each switch.
    """
    path = project / "specs.toml"
    text = path.read_text(encoding="utf-8")
    for name, value in switches.items():
        text = text.replace(f"\n{name} = true\n", f"\n{name} = {str(value).lower()}\n").replace(
            f"\n{name} = false\n", f"\n{name} = {str(value).lower()}\n"
        )
    path.write_text(text, encoding="utf-8")


PARTS = (
    ".mcp.json",
    ".claude/skills/spec-write/SKILL.md",
    ".github/workflows/specs.yml",
    "AGENTS.md",
    "CLAUDE.md",
)


def test_a_switch_off_removes_the_part(kit: Kit, project: Path) -> None:
    """`specs install` removes each part whose switch is off."""
    _switch(project, mcp=False, skills=False, ci=False, agents=False, claude=False)
    result = kit.run(project, "install", "--raw")
    assert result.code == 0, result.out + result.err
    for name in PARTS:
        assert not (project / name).exists(), name
        assert f"D {name}" in result.out, name


def test_a_switch_on_writes_the_part_again(kit: Kit, project: Path) -> None:
    """`specs install` writes a part again when its switch is on again."""
    _switch(project, mcp=False, skills=False, ci=False, agents=False, claude=False)
    assert kit.run(project, "install").code == 0
    _switch(project, mcp=True, skills=True, ci=True, agents=True, claude=True)
    result = kit.run(project, "install", "--raw")
    assert result.code == 0, result.out + result.err
    for name in PARTS:
        assert (project / name).is_file(), name


def test_a_changed_claude_file_stays(kit: Kit, project: Path) -> None:
    """A `CLAUDE.md` with more text stays, and install shows the line to remove."""
    path = project / "CLAUDE.md"
    path.write_text("@AGENTS.md\n\nMy notes.\n", encoding="utf-8")
    _switch(project, claude=False)
    result = kit.run(project, "install", "--raw")
    assert result.code == 0, result.out + result.err
    assert path.is_file()
    assert "remove the line @AGENTS.md from CLAUDE.md" in result.out


def test_claude_needs_agents(kit: Kit, project: Path) -> None:
    """`claude = true` with `agents = false` stops each command with an error."""
    _switch(project, agents=False)
    result = kit.run(project, "check", "--raw")
    assert result.code == 1
    assert "features.claude needs features.agents" in result.err


def test_update_follows_the_switches(kit: Kit, project: Path) -> None:
    """`specs update` of the kit writes no part whose switch is off."""
    _switch(project, skills=False, mcp=False)
    result = kit.run(project, "update", "kit", kit.rev, "--raw")
    assert result.code == 0, result.out + result.err
    assert not (project / ".claude/skills").exists()
    assert not (project / ".mcp.json").exists()
