"""Tests of `specs new` (§000069, §000008)."""

from __future__ import annotations

from pathlib import Path

from conftest import Kit, git


def _new(kit: Kit, project: Path, *args: str) -> tuple[int, str, str]:
    """Run `specs new` with an owner.

    Args:
        kit: The kit.
        project: The root of the project.
        *args: The arguments after `new`.

    Returns:
        The exit code, stdout and stderr.
    """
    result = kit.run(project, "new", *args, "--owner", "someone", "--raw")
    return result.code, result.out, result.err


def test_new_writes_a_spec_that_passes_the_check(kit: Kit, project: Path) -> None:
    """`specs new` writes the next number, the keys and the scope, and the copy passes the check."""
    (project / "src").mkdir()
    code, out, err = _new(
        kit, project, "F", "app/login", "sign-in", "Sign in with a \\d key", "--scope", "src"
    )
    path = project / "specs/requirements/functional/app/login/000001_sign-in.md"
    text = path.read_text(encoding="utf-8")
    assert code == 0, out + err
    assert 'id: "000001"' in text
    assert "title: Sign in with a \\d key" in text
    assert "scope:\n  - src\n" in text
    assert "# Sign in with a \\d key" in text
    assert "A specs/requirements/functional/app/login/000001_sign-in.md" in out
    check = kit.run(project, "install", "--raw")
    assert "000001" not in check.out.replace("specs, 0 errors", "")


def test_new_writes_a_schema_for_a_json_protocol(kit: Kit, project: Path) -> None:
    """`specs new` writes a minimal JSON Schema next to a protocol with a JSON media type."""
    (project / "src").mkdir()
    code, out, err = _new(kit, project, "P", "api/events", "event", "An event", "--scope", "src")
    assert code == 0, out + err
    assert (project / "specs/protocols/api/events/000001_event.schema.json").is_file()


def test_new_stops_for_a_missing_scope_path(kit: Kit, project: Path) -> None:
    """`specs new` stops with an error and writes no file when a scope path does not exist."""
    code, _, err = _new(kit, project, "F", "app/login", "sign-in", "Sign in", "--scope", "nope")
    assert code == 1
    assert "nope" in err
    assert not (project / "specs/requirements").exists()


def test_new_needs_a_scope(kit: Kit, project: Path) -> None:
    """`--scope` is required."""
    code, _, err = _new(kit, project, "F", "app/login", "sign-in", "Sign in")
    assert code == 2
    assert "--scope" in err


def test_new_skips_the_numbers_of_the_copies(kit: Kit, project: Path) -> None:
    """The next number counts the rules of the project on the base branch, not the copies."""
    (project / "src").mkdir()
    (project / "src/app.py").write_text("x = 1\n", encoding="utf-8")
    git(project, "add", "-A", env=kit.env)
    git(project, "commit", "-q", "-m", "start", env=kit.env)
    git(project, "update-ref", "refs/remotes/origin/main", "HEAD", env=kit.env)
    code, out, err = _new(kit, project, "F", "app/login", "sign-in", "Sign in", "--scope", "src")
    assert code == 0, out + err
    assert (project / "specs/requirements/functional/app/login/000001_sign-in.md").is_file()
