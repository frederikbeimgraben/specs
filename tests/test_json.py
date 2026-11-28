"""Tests of the JSON output (§000080)."""

from __future__ import annotations

import json
from pathlib import Path

from conftest import Kit

LONG = "github.com/frederikbeimgraben/spezi:W/specs/process/000001"
PATH = (
    "specs/.upstream/github.com/frederikbeimgraben/spezi/workflow/specs/process/"
    "000001_precedence.md"
)
RULE = {
    "kind": "W",
    "id": "github.com/frederikbeimgraben/spezi:000001",
    "long": LONG,
    "status": "approved",
    "title": "A spec wins over other guidance",
    "path": PATH,
}


def _json(kit: Kit, project: Path, *args: str) -> object:
    """Run a command with `--json` and parse its stdout.

    Args:
        kit: The kit.
        project: The folder to run in.
        *args: The arguments before `--json`.

    Returns:
        The parsed value.
    """
    return json.loads(kit.run(project, *args, "--json").out)


def test_list_and_resolve_give_rules(kit: Kit, project: Path) -> None:
    """`specs list` gives a list of rule objects, and `specs resolve` gives one of them."""
    listed = _json(kit, project, "list")
    assert isinstance(listed, list)
    assert RULE in listed
    assert _json(kit, project, "resolve", LONG) == RULE


def test_show_gives_meta_and_body(kit: Kit, project: Path) -> None:
    """`specs show` gives the front matter as an object and the body."""
    shown = _json(kit, project, "show", LONG)
    assert isinstance(shown, dict)
    assert shown["long"] == LONG
    assert shown["path"] == PATH
    assert shown["meta"]["status"] == "approved"
    assert str(shown["body"]).lstrip().startswith("# A spec wins over other guidance")


def test_check_gives_errors_as_objects(kit: Kit, project: Path) -> None:
    """`specs check` gives the count, each error as an object, and the changed files."""
    (project / "specs" / "README.md").write_text("changed\n", encoding="utf-8")
    result = kit.run(project, "check", "--json")
    checked = json.loads(result.out)
    assert result.code == 1
    assert checked["changed"] == []
    assert {
        "file": "specs/README.md",
        "line": 1,
        "message": "the index is not current; run spezi install",
        "rule": "000007",
    } in checked["errors"]


def test_a_command_that_changes_files_gives_all_parts(kit: Kit, project: Path) -> None:
    """`specs new` gives the message, the hints, no check and the changed files."""
    (project / "src").mkdir()
    made = _json(
        kit,
        project,
        "new",
        "F",
        "app/login",
        "sign-in",
        "Sign in",
        "--scope",
        "src",
        "--owner",
        "someone",
    )
    path = "specs/requirements/functional/app/login/000001_sign-in.md"
    assert made == {
        "message": path,
        "hints": [],
        "check": None,
        "changed": [{"mark": "A", "path": path}],
    }


def test_a_stop_gives_an_error_object(kit: Kit, project: Path) -> None:
    """A command that stops prints an error object to stdout and ends with exit code 1."""
    result = kit.run(project, "resolve", "999999", "--json")
    assert result.code == 1
    assert result.err == ""
    assert json.loads(result.out) == {"error": "999999 names no rule"}


def test_raw_and_json_exclude_each_other(kit: Kit, project: Path) -> None:
    """`--raw` and `--json` must not go together; with `--json` the stop is an error object."""
    result = kit.run(project, "list", "--raw", "--json")
    assert result.code == 1
    assert result.err == ""
    assert "not allowed" in json.loads(result.out)["error"]
    plain = kit.run(project, "list", "--raw", "--bad")
    assert plain.code == 2
    assert "unrecognized arguments" in plain.err
