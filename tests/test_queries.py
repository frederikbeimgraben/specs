"""Tests of `specs resolve`, `show`, `list` and `search` (§000070 to §000073)."""

from __future__ import annotations

from pathlib import Path

from conftest import Kit

LONG = "github.com/frederikbeimgraben/specs:W/specs/process/000001"


def test_resolve_prints_the_long_form(kit: Kit, project: Path) -> None:
    """`specs resolve` prints the long form for a short and a long form."""
    assert (
        kit.run(project, "resolve", "github.com/frederikbeimgraben/specs:000001", "--raw").out
        == f"{LONG}\n"
    )
    assert kit.run(project, "resolve", LONG, "--raw").out == f"{LONG}\n"


def test_resolve_stops_for_an_unknown_id(kit: Kit, project: Path) -> None:
    """`specs resolve` stops with an error when no rule has the ID."""
    result = kit.run(project, "resolve", "999999", "--raw")
    assert result.code == 1
    assert "999999" in result.err


def test_show_prints_the_full_text(kit: Kit, project: Path) -> None:
    """`specs show` prints the full text of the spec file."""
    path = (
        project
        / "specs/.upstream/github.com/frederikbeimgraben/specs/workflow/specs/process"
        / "000001_precedence.md"
    )
    assert kit.run(project, "show", LONG, "--raw").out == path.read_text(encoding="utf-8")


def test_show_stops_for_an_unknown_id(kit: Kit, project: Path) -> None:
    """`specs show` stops with an error when no rule has the ID."""
    assert kit.run(project, "show", "999999", "--raw").code == 1


def test_list_prints_one_line_for_each_rule(kit: Kit, project: Path) -> None:
    """`specs list` prints kind letter, short form, status and title, separated by tabs."""
    lines = kit.run(project, "list", "--raw").out.splitlines()
    assert (
        "W\tgithub.com/frederikbeimgraben/specs:000001\tapproved\tA spec wins over other "
        "guidance" in lines
    )
    assert all(len(line.split("\t")) == 4 for line in lines)


def test_list_filters_by_kind(kit: Kit, project: Path) -> None:
    """`specs list <kind>` prints only the rules of this kind, for a name or a letter."""
    by_letter = kit.run(project, "list", "A", "--raw").out
    assert by_letter == kit.run(project, "list", "agent", "--raw").out
    assert by_letter
    assert all(line.startswith("A\t") for line in by_letter.splitlines())
    unknown = kit.run(project, "list", "nothing", "--raw")
    assert unknown.code == 1
    assert "unknown kind" in unknown.err


def test_search_ignores_the_case(kit: Kit, project: Path) -> None:
    """`specs search` finds rules by title or body, and case does not change the result."""
    upper = kit.run(project, "search", "ASSUMPTION", "--raw").out
    lower = kit.run(project, "search", "assumption", "--raw").out
    assert upper == lower
    assert "000044" in upper
