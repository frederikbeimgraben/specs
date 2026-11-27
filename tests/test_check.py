"""Tests of `specs check` and of the checks of the conventions (§000065, §000007)."""

from __future__ import annotations

from pathlib import Path

from conftest import Kit, write_rule


def _rule(project: Path, text: str = "A name must be short.") -> Path:
    """Write one valid style rule to the project.

    Args:
        project: The root of the project.
        text: The rule text.

    Returns:
        The file.
    """
    (project / "src").mkdir(exist_ok=True)
    return write_rule(
        project, "style/code/names", "000100", "short-names", "Names are short", "style", text
    )


def test_check_passes_after_init(kit: Kit, project: Path) -> None:
    """A new project has no errors and exit code 0."""
    result = kit.run(project, "check", "--raw")
    assert result.code == 0
    assert result.out.endswith("0 specs, 0 errors\n")


def test_check_without_write_changes_no_file(kit: Kit, project: Path) -> None:
    """`specs check` must not change a file."""
    _rule(project)
    before = (project / "specs" / "README.md").read_text(encoding="utf-8")
    result = kit.run(project, "check", "--raw")
    assert result.code == 1
    assert "the index is not current" in result.out
    assert (project / "specs" / "README.md").read_text(encoding="utf-8") == before


def test_check_write_writes_the_index(kit: Kit, project: Path) -> None:
    """`specs install` writes the index."""
    _rule(project)
    result = kit.run(project, "install", "--raw")
    index = (project / "specs" / "README.md").read_text(encoding="utf-8")
    assert result.code == 0, result.out
    assert "S/code/names/000100" in index


def test_check_finds_a_rule_without_must(kit: Kit, project: Path) -> None:
    """A rule text without `must` is an error with exit code 1."""
    _rule(project, "A name is short.")
    result = kit.run(project, "install", "--raw")
    assert result.code == 1
    assert "000100" in result.out


def test_check_finds_a_bad_file_name(kit: Kit, project: Path) -> None:
    """A file name that breaks the convention is an error."""
    path = _rule(project)
    path.rename(path.with_name("100_short.md"))
    result = kit.run(project, "install", "--raw")
    assert result.code == 1
    assert "100_short.md" in result.out


def test_check_finds_a_missing_key(kit: Kit, project: Path) -> None:
    """A front matter without `owner` is an error."""
    path = _rule(project)
    path.write_text(
        path.read_text(encoding="utf-8").replace("owner: someone\n", ""), encoding="utf-8"
    )
    result = kit.run(project, "install", "--raw")
    assert result.code == 1
    assert "front matter keys" in result.out


def test_check_finds_a_stale_index(kit: Kit, project: Path) -> None:
    """`specs check` fails when the index is not current."""
    (project / "specs" / "README.md").write_text("changed\n", encoding="utf-8")
    result = kit.run(project, "check", "--raw")
    assert result.code == 1
    assert "the index is not current" in result.out
