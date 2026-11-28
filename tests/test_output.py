"""Tests of the output of the command (spec 000076, 000077) and of the MCP tools (spec 000074)."""

from __future__ import annotations

import os
import pty
import re
import subprocess
import sys
from pathlib import Path

import pytest
from conftest import Kit

ANSI = re.compile(r"\x1b\[")


def _on_terminal(kit: Kit, cwd: Path, *args: str, extra: tuple[tuple[str, str], ...] = ()) -> str:
    """Run the command with stdout and stderr on a terminal and return its output.

    Args:
        kit: The kit.
        cwd: The folder to run in.
        *args: The arguments.
        extra: More environment variables.

    Returns:
        The output.
    """
    main, side = pty.openpty()
    with subprocess.Popen(
        (sys.executable, "-m", "spezi", *args),
        cwd=cwd,
        env={**kit.env, "COLUMNS": "200", "TERM": "xterm-256color", **dict(extra)},
        stdout=side,
        stderr=side,
    ) as process:
        os.close(side)
        chunks: list[bytes] = []
        while True:
            try:
                chunk = os.read(main, 4096)
            except OSError:
                break
            if not chunk:
                break
            chunks.append(chunk)
        process.wait()
    os.close(main)
    return b"".join(chunks).decode("utf-8", "replace")


def test_terminal_output_has_color(kit: Kit, project: Path) -> None:
    """On a terminal, the output is formatted."""
    assert ANSI.search(_on_terminal(kit, project, "check"))


def test_raw_output_has_no_color(kit: Kit, project: Path) -> None:
    """With `--raw`, the output is plain text also on a terminal."""
    assert not ANSI.search(_on_terminal(kit, project, "list", "--raw"))


def test_help_on_terminal_has_color(kit: Kit, project: Path) -> None:
    """On a terminal, the help of `spezi` and of a command has color."""
    assert ANSI.search(_on_terminal(kit, project, "--help"))
    assert ANSI.search(_on_terminal(kit, project, "list", "--help"))


def test_usage_on_terminal_has_color(kit: Kit, project: Path) -> None:
    """On a terminal, the usage after a wrong argument has color."""
    assert ANSI.search(_on_terminal(kit, project, "list", "--wrong"))


def test_help_with_no_color_has_no_color(kit: Kit, project: Path) -> None:
    """With `NO_COLOR`, the help and the usage are plain text also on a terminal."""
    assert not ANSI.search(_on_terminal(kit, project, "--help", extra=(("NO_COLOR", "1"),)))
    assert not ANSI.search(
        _on_terminal(kit, project, "list", "--wrong", extra=(("NO_COLOR", "1"),))
    )


def test_help_in_a_pipe_has_no_color(kit: Kit, project: Path) -> None:
    """In a pipe, the help and the usage are plain text, with the words of argparse."""
    env = {**kit.env, "FORCE_COLOR": "1"}
    shown = subprocess.run(
        (sys.executable, "-m", "spezi", "--help"), cwd=project, env=env, capture_output=True
    )
    wrong = subprocess.run(
        (sys.executable, "-m", "spezi", "list", "--wrong"),
        cwd=project,
        env=env,
        capture_output=True,
    )
    assert shown.stdout.startswith(b"usage: spezi")
    assert not ANSI.search(shown.stdout.decode())
    assert wrong.returncode == 2
    assert wrong.stderr.startswith(b"usage: spezi")
    assert not ANSI.search(wrong.stderr.decode())


def test_changed_files_are_sorted_and_relative(kit: Kit, empty: Path) -> None:
    """A command lists each changed file once, sorted, relative, as in `git status --short`."""
    lines = [
        line
        for line in kit.run(empty, "init", "--forge", "github", "--raw").out.splitlines()
        if re.match(r"^[AMD] ", line)
    ]
    paths = [line[2:] for line in lines]
    assert paths == sorted(paths, key=lambda p: Path(p).parts)
    assert "A spezi.toml" in lines
    assert all(not p.startswith("/") for p in paths)


def test_the_report_comes_after_the_files(kit: Kit, empty: Path) -> None:
    """The changed files come before the report of the check, and the report is the last line."""
    out = kit.run(empty, "init", "--forge", "github", "--raw").out.splitlines()
    assert re.fullmatch(r"[0-9]+ specs, [0-9]+ upstream, [0-9]+ errors", out[-1])
    assert max(i for i, line in enumerate(out) if re.match(r"^[AMD] ", line)) < len(out) - 1


def test_a_write_with_the_same_content_is_no_change(kit: Kit, project: Path) -> None:
    """`specs install` on a current project lists no file."""
    out = kit.run(project, "install", "--raw").out
    assert not [line for line in out.splitlines() if re.match(r"^[AMD] ", line)]


def test_mcp_tools_give_the_plain_results(
    kit: Kit, project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The MCP tools give the same results as the commands, and only `install` writes the index."""
    for key, value in kit.env.items():
        monkeypatch.setenv(key, value)
    monkeypatch.chdir(project)
    from spezi import mcp_server

    (project / "specs" / "README.md").write_text("changed\n", encoding="utf-8")
    assert "the index is not current" in mcp_server.check()
    assert (project / "specs" / "README.md").read_text(encoding="utf-8") == "changed\n"
    assert "M specs/README.md" in mcp_server.install()
    assert "the index is not current" not in mcp_server.check()
    assert mcp_server.list_specs() == kit.run(project, "list", "--raw").out
    (project / "src").mkdir()
    result = mcp_server.new("F", "app/login", "sign-in", "Sign in", ["src"], "someone")
    assert "A specs/requirements/functional/app/login/000001_sign-in.md" in result
