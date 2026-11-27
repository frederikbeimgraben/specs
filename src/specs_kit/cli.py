"""The command `specs`: check and manage the specs of a project.

Usage:
    specs check [--write]
    specs init [<dir>] [--forge github|gitlab|codeberg]
    specs update [<ref>]
    specs update <repo> <ref>
    specs add <repo> <ref> [--include <folder>]...
    specs new <kind> <area>/<topic> <name> "<title>" --scope <path>... [--owner <login>]
    specs resolve <id>
    specs show <id>
    specs list
    specs search <text>
    specs mcp
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable, Mapping
from pathlib import Path

from rich.console import Group, RenderableType
from rich.text import Text

from specs_kit import queries
from specs_kit.changes import Mark, lines, recording
from specs_kit.check import run
from specs_kit.devshell import init_flake, update_flake
from specs_kit.kit import KitError, add, init, update
from specs_kit.mcp_server import serve
from specs_kit.new import NewError, new
from specs_kit.project import KIT_REPO, ConfigError, Project
from specs_kit.view import console, done, file_list, report, spec_text, table


def parser() -> argparse.ArgumentParser:
    """Return the parser of the command line."""
    root = argparse.ArgumentParser(
        prog="specs", description="Check and manage the specs of a project."
    )
    commands = root.add_subparsers(dest="command", required=True)
    check = commands.add_parser("check", help="check the specs; --write also writes the index")
    check.add_argument("--write", action="store_true")
    start = commands.add_parser("init", help="install the kit in a project")
    start.add_argument("dir", nargs="?", default=".")
    start.add_argument("--forge", choices=("github", "gitlab", "codeberg"))
    renew = commands.add_parser("update", help="update the kit, or the copy of one repository")
    renew.add_argument("args", nargs="*", metavar="[repo] ref")
    more = commands.add_parser("add", help="add the copy of a repository")
    more.add_argument("repo")
    more.add_argument("ref")
    more.add_argument("--include", action="append", default=[], metavar="folder")
    create = commands.add_parser("new", help="create a new spec from its template")
    create.add_argument("kind")
    create.add_argument("path", metavar="area/topic")
    create.add_argument("name")
    create.add_argument("title")
    create.add_argument("--owner")
    create.add_argument(
        "--scope", action="append", required=True, metavar="path", help="a path of the rule"
    )
    commands.add_parser("resolve", help="print the long form of a rule ID").add_argument("id")
    commands.add_parser("show", help="print the full text of a spec").add_argument("id")
    commands.add_parser("list", help="list every rule")
    commands.add_parser("search", help="list the rules that hold a text").add_argument("text")
    for name, sub in commands.choices.items():
        if name != "mcp":
            sub.add_argument(
                "--raw", action="store_true", help="print plain text, also without a terminal"
            )
    commands.add_parser("mcp", help="run the MCP server on stdin and stdout")
    return root


def _update_target(args: list[str]) -> tuple[str, str | None]:
    """Return the repository and the ref of `specs update`.

    Args:
        args: The arguments after `update`.

    Returns:
        The repository and the ref, or None for the default branch.

    Raises:
        KitError: More than two arguments.
    """
    match args:
        case []:
            return KIT_REPO, None
        case [ref]:
            return KIT_REPO, ref
        case [repo, ref]:
            return repo, ref
        case _:
            raise KitError("usage: specs update [<repo>] [<ref>]")


def _pretty(args: argparse.Namespace) -> bool:
    """Return True for the formatted output (§000076).

    Args:
        args: The parsed command line.

    Returns:
        True without `--raw` when stdout is a terminal.
    """
    return not bool(getattr(args, "raw", False)) and sys.stdout.isatty()


def _emit(pretty: bool, raw: Callable[[], str], view: Callable[[], RenderableType]) -> int:
    """Print the formatted or the plain output.

    Args:
        pretty: True for the formatted output.
        raw: The plain text.
        view: The formatted output.

    Returns:
        The exit code 0.
    """
    match pretty:
        case True:
            console().print(view())
        case False:
            text = raw()
            sys.stdout.write(text if text.endswith("\n") or not text else f"{text}\n")
    return 0


def _raw_changes(changed: tuple[tuple[Mark, str], ...]) -> str:
    """Return the changed files as plain text, one `<mark> <path>` on each line (§000077).

    Args:
        changed: The mark and the path of each change.

    Returns:
        The lines, each with a newline.
    """
    return "".join(f"{mark} {path}\n" for mark, path in changed)


def _check(
    write: bool,
    pretty: bool,
    log: Mapping[Path, Mark],
    head: tuple[str, ...] = (),
    root: Path | None = None,
) -> int:
    """Run the check and print the messages, the report and the changed files.

    `update` and `add` run the check with `--write` at their end and give their message as
    `head` (§000067, §000068).

    Args:
        write: True to write the index first.
        pretty: True for the formatted output.
        log: The changes of the command.
        head: The messages of the command before the check, or empty.
        root: The root of the project, or None to search from the current folder.

    Returns:
        The exit code: 1 when the check finds errors.
    """
    project = Project.open(root)
    count, errors = run(project, write=write)
    changed = lines(log, project.root)
    _emit(
        pretty,
        lambda: (
            "".join(f"{h}\n" for h in head)
            + "".join(f"{e}\n" for e in errors)
            + f"{count} specs, {len(errors)} errors\n"
            + _raw_changes(changed)
        ),
        lambda: Group(*(done(h) for h in head), report(count, tuple(errors)), file_list(changed)),
    )
    return 1 if errors else 0


def _message(pretty: bool, text: str, log: Mapping[Path, Mark], root: Path) -> int:
    """Print the message of a command that changes files, and the changed files.

    Args:
        pretty: True for the formatted output.
        text: The message.
        log: The changes of the command.
        root: The root of the project.

    Returns:
        The exit code 0.
    """
    changed = lines(log, root)
    return _emit(
        pretty,
        lambda: f"{text}\n{_raw_changes(changed)}",
        lambda: Group(done(text), file_list(changed)),
    )


def _lines(text: str, hints: tuple[str, ...]) -> str:
    """Return a message with its hints below it.

    Args:
        text: The message.
        hints: The hints.

    Returns:
        The message and one hint on each line.
    """
    return "\n".join((text, *hints))


def dispatch(args: argparse.Namespace) -> int:
    """Run one command and record the files it changes.

    Args:
        args: The parsed command line.

    Returns:
        The exit code.
    """
    with recording() as log:
        return _dispatch(args, _pretty(args), log)


def _dispatch(args: argparse.Namespace, pretty: bool, log: Mapping[Path, Mark]) -> int:
    """Run one command.

    Args:
        args: The parsed command line.
        pretty: True for the formatted output.
        log: The changes of the command, filled while it runs.

    Returns:
        The exit code.
    """
    command: str = args.command
    match command:
        case "check":
            return _check(bool(args.write), pretty, log)
        case "init":
            project = init(Path(args.dir), args.forge)
            hints = init_flake(project.root, project.config.upstream.get(KIT_REPO) or "")
            text = _lines(f"installed the kit in {project.root}", hints)
            return _check(True, pretty, log, (text,), project.root)
        case "update":
            target = _update_target(list(args.args))
            project = Project.open()
            commit = update(project, *target)
            hints = update_flake(project.root, commit) if target[0] == KIT_REPO else ()
            return _check(True, pretty, log, (_lines(f"updated to {commit}", hints),))
        case "add":
            project = Project.open()
            commit = add(project, args.repo, args.ref, tuple(args.include))
            return _check(True, pretty, log, (f"added at {commit}",))
        case "new":
            project = Project.open()
            path = new(
                project, args.kind, args.path, args.name, args.title, args.owner, tuple(args.scope)
            )
            return _message(pretty, str(path), log, project.root)
        case "resolve":
            long = queries.resolve(Project.open(), args.id)
            return _emit(pretty, lambda: long, lambda: Text(long, style="bold cyan"))
        case "show":
            text = queries.show(Project.open(), args.id)
            return _emit(pretty, lambda: text, lambda: spec_text(text))
        case "list":
            project = Project.open()
            return _emit(
                pretty, lambda: queries.listing(project), lambda: table(project.all_specs())
            )
        case "search":
            project = Project.open()
            return _emit(
                pretty,
                lambda: queries.search(project, args.text),
                lambda: table(queries.matches(project, args.text)),
            )
        case "mcp":
            return serve()
        case _:
            raise KitError(f"unknown command {command!r}")


def main() -> None:
    """Run the command line and exit with its code."""
    try:
        sys.exit(dispatch(parser().parse_args()))
    except (KitError, NewError, ConfigError, queries.QueryError, OSError) as error:
        sys.exit(f"specs: {error}")
