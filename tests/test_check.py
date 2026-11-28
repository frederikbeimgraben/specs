"""Tests of `specs check` and of the checks of the conventions (spec 000065, 000007)."""

from __future__ import annotations

import json
import re
from pathlib import Path

from conftest import Kit, git, write_rule


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
    """A new project has no errors and exit code 0, and the check counts the rules of the kit."""
    result = kit.run(project, "check", "--raw")
    assert result.code == 0
    assert re.search(r"(^|\n)0 specs, [1-9][0-9]* upstream, 0 errors, 0 warnings\n$", result.out)


def test_check_changes_no_file(kit: Kit, project: Path) -> None:
    """`specs check` must not change a file."""
    _rule(project)
    before = (project / "specs" / "README.md").read_text(encoding="utf-8")
    result = kit.run(project, "check", "--raw")
    assert result.code == 1
    assert "the index is not current" in result.out
    assert (project / "specs" / "README.md").read_text(encoding="utf-8") == before


def test_install_writes_the_index(kit: Kit, project: Path) -> None:
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


def test_check_gives_the_line(kit: Kit, project: Path) -> None:
    """An error line names the line of the key or of the reference, else line 1."""
    path = _rule(project, "A name must be short, as §000999 says.")
    path.write_text(
        path.read_text(encoding="utf-8").replace("updated: 2026-11-27", "updated: today"),
        encoding="utf-8",
    )
    result = kit.run(project, "check", "--raw")
    rel = "specs/style/code/names/000100_short-names.md"
    assert f"{rel}:7: updated must be YYYY-MM-DD (000009)" in result.out
    assert f"{rel}:15: use (spec 000999) in place of §000999 (000017)" in result.out
    assert "specs/README.md:1: the index is not current" in result.out


def test_check_finds_a_file_outside_the_kind_folders(kit: Kit, project: Path) -> None:
    """A file of each type that is not below a kind folder is an error of 000051."""
    (project / "specs/notes").mkdir()
    (project / "specs/notes/todo.txt").write_text("x\n", encoding="utf-8")
    result = kit.run(project, "check", "--raw")
    assert result.code == 1
    assert "specs/notes/todo.txt:1: not below a kind folder (000051)" in result.out


def test_check_gives_the_line_of_the_key(kit: Kit, project: Path) -> None:
    """An error of a key names the line of the key, also when an other line has the value."""
    path = _rule(project)
    path.write_text(
        path.read_text(encoding="utf-8")
        .replace("title: Names are short", "title: Names are functional")
        .replace("kind: style", "kind: functional"),
        encoding="utf-8",
    )
    result = kit.run(project, "check", "--raw")
    rel = "specs/style/code/names/000100_short-names.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    assert f"{rel}:{lines.index('kind: functional') + 1}: kind 'functional'" in result.out


def test_check_finds_an_old_diagram_type(kit: Kit, project: Path) -> None:
    """A state diagram must start with `stateDiagram-v2`, not with `stateDiagram`."""
    name = "specs/structures/specs/lifecycle/000041_status-life-cycle.md"
    path = project / name
    path.parent.mkdir(parents=True)
    path.write_text(
        (kit.source / name).read_text(encoding="utf-8").replace("stateDiagram-v2", "stateDiagram"),
        encoding="utf-8",
    )
    result = kit.run(project, "check", "--raw")
    assert result.code == 1
    assert "a state diagram must start with stateDiagram-v2 (000034)" in result.out


def test_check_finds_a_reference_to_no_rule(kit: Kit, project: Path) -> None:
    """A number in the text of a spec must name a rule of the project."""
    _rule(project, "A name must be short (spec 000999).")
    result = kit.run(project, "check", "--raw")
    assert result.code == 1
    assert "000999 names no rule of the project (000047)" in result.out


def test_check_finds_a_reference_to_a_removed_rule(kit: Kit, project: Path) -> None:
    """A reference in a spec or in the code must not name a rule that is not in force."""
    _rule(project, "A name must be short (spec 000101).")
    old = write_rule(
        project, "style/code/names", "000101", "old-names", "Old names", "style", "Old: must go."
    )
    old.write_text(
        old.read_text(encoding="utf-8").replace("status: approved", "status: removed"),
        encoding="utf-8",
    )
    (project / "src/app.py").write_text('"""See (spec 000101)."""\n', encoding="utf-8")
    path = project / "spezi.toml"
    path.write_text(
        path.read_text(encoding="utf-8").replace("code_dirs = []", 'code_dirs = ["src"]'),
        encoding="utf-8",
    )
    result = kit.run(project, "check", "--raw")
    assert result.code == 1
    assert "000101 names a rule with the status removed (000047)" in result.out
    assert "src/app.py:1: 000101 names a rule with the status removed (000047)" in result.out


def test_check_finds_a_bare_number_in_a_spec(kit: Kit, project: Path) -> None:
    """A rule number in the text of a spec must stand in `(spec ...)` (000017)."""
    _rule(project, "A name must be short, as 000101 says. See `000102` and (spec 000100).")
    result = kit.run(project, "check", "--raw")
    assert result.code == 1
    assert "a rule number must stand in (spec ...) (000017): '000101'" in result.out
    assert "000102" not in result.out
    assert "000100" not in result.out.replace("000100_short-names", "")


def test_check_finds_a_bad_reference(kit: Kit, project: Path) -> None:
    """A `(spec ...)` reference holds only short forms, with `, ` between them (000017)."""
    _rule(project, "A name must be short (spec 000100 to 000102).")
    result = kit.run(project, "check", "--raw")
    assert result.code == 1
    assert "(spec 000100 to 000102) must hold only short forms of rules" in result.out


def test_check_reads_each_item_of_a_list(kit: Kit, project: Path) -> None:
    """Each item of a list must name a rule that exists (000017)."""
    _rule(project, "A name must be short (spec 000100, 000999).")
    result = kit.run(project, "check", "--raw")
    assert result.code == 1
    assert "000999 names no rule of the project (000047)" in result.out


def test_check_finds_an_old_reference_in_the_code(kit: Kit, project: Path) -> None:
    """A code file of `code_dirs` must not refer to a rule with `§` (spec 000017)."""
    _rule(project)
    (project / "src").mkdir(exist_ok=True)
    (project / "src/app.py").write_text('"""See §000100."""\n', encoding="utf-8")
    path = project / "spezi.toml"
    path.write_text(
        path.read_text(encoding="utf-8").replace("code_dirs = []", 'code_dirs = ["src"]'),
        encoding="utf-8",
    )
    result = kit.run(project, "check", "--raw")
    assert result.code == 1
    assert "src/app.py:1: use (spec 000100) in place of §000100 (000017)" in result.out


def test_check_reads_each_markdown_file_that_git_tracks(kit: Kit, project: Path) -> None:
    """A Markdown file outside `specs/` follows the rule when git tracks it (000017)."""
    _rule(project)
    (project / "docs").mkdir()
    (project / "docs/guide.md").write_text("See 000100.\n", encoding="utf-8")
    (project / "docs/notes.md").write_text("See 000100.\n", encoding="utf-8")
    git(project, "add", "docs/guide.md")
    result = kit.run(project, "check", "--raw")
    assert result.code == 1
    error = "docs/guide.md:1: a rule number must stand in (spec ...) (000017): '000100'"
    assert error in result.out
    assert "docs/notes.md" not in result.out


def test_check_finds_front_matter_that_is_no_yaml(kit: Kit, project: Path) -> None:
    """A front matter that is no valid YAML is an error of 000009."""
    path = _rule(project)
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "title: Names are short", "title: Names: are short"
        ),
        encoding="utf-8",
    )
    result = kit.run(project, "check", "--raw")
    assert result.code == 1
    assert "front matter: no valid YAML" in result.out
    assert "(000009)" in result.out


def test_check_finds_a_rule_of_a_copy_that_it_cannot_read(kit: Kit, project: Path) -> None:
    """A rule of a copy without front matter is an error, and the check does not count it."""
    copy = project / "specs/.upstream/github.com/frederikbeimgraben/spezi"
    before = kit.run(project, "check", "--json")
    rule = next(copy.glob("workflow/specs/process/000001_*.md"))
    rule.write_text("No front matter.\n", encoding="utf-8")
    result = kit.run(project, "check", "--raw")
    rel = rule.relative_to(project).as_posix()
    assert result.code == 1
    assert f"{rel}:1: no front matter (000009)" in result.out
    assert json.loads(kit.run(project, "check", "--json").out)["upstream"] == (
        json.loads(before.out)["upstream"] - 1
    )


def test_check_finds_a_reference_to_an_own_rule_in_a_skill(kit: Kit, project: Path) -> None:
    """A file that a project gets must not name a rule of the project in a folder of `own`."""
    write_rule(project, "style/code/names", "000101", "names", "Names", "style", "Names: must.")
    config = project / "spezi.toml"
    config.write_text(
        config.read_text(encoding="utf-8").replace("own = []", 'own = ["style/"]'),
        encoding="utf-8",
    )
    skill = project / ".claude/skills/spezi-check/SKILL.md"
    text = skill.read_text(encoding="utf-8")
    skill.write_text(f"{text}\nSee (spec 000101).\n", encoding="utf-8")
    line = len(text.splitlines()) + 2
    result = kit.run(project, "check", "--raw")
    assert result.code == 1
    assert f".claude/skills/spezi-check/SKILL.md:{line}: (spec 000101) names a rule of own" in (
        result.out
    )
