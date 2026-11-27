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
    specs list [<kind>]
    specs search <text>
    specs mcp

Each command except `mcp` takes `--raw` or `--json`.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable, Mapping
from enum import Enum, auto
from pathlib import Path

from rich.console import Group, RenderableType
from rich.text import Text

from specs_kit import data, queries
from specs_kit.agents import claude_import
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
    commands.add_parser("list", help="list every rule, or the rules of one kind").add_argument(
        "kind", nargs="?", help="a kind name or a kind letter"
    )
    commands.add_parser("search", help="list the rules that hold a text").add_argument("text")
    for name, sub in commands.choices.items():
        if name != "mcp":
            form = sub.add_mutually_exclusive_group()
            form.add_argument("--raw", action="store_true", help="print plain text")
            form.add_argument("--json", action="store_true", help="print the data as JSON")
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


class Mode(Enum):
    """The form of the output (§000076, §000080)."""

    PRETTY = auto()
    RAW = auto()
    JSON = auto()


def _mode(args: argparse.Namespace) -> Mode:
    """Return the form of the output.

    Args:
        args: The parsed command line.

    Returns:
        JSON with `--json`, the formatted output on a terminal without `--raw`, else plain text.
    """
    match bool(getattr(args, "json", False)), bool(getattr(args, "raw", False)):
        case True, _:
            return Mode.JSON
        case False, False if sys.stdout.isatty():
            return Mode.PRETTY
        case _:
            return Mode.RAW


def _emit(
    mode: Mode,
    raw: Callable[[], str],
    view: Callable[[], RenderableType],
    value: Callable[[], data.Json],
) -> int:
    """Print the formatted output, the plain output or the JSON.

    Args:
        mode: The form of the output.
        raw: The plain text.
        view: The formatted output.
        value: The data for JSON.

    Returns:
        The exit code 0.
    """
    match mode:
        case Mode.PRETTY:
            console().print(view())
        case Mode.RAW:
            text = raw()
            sys.stdout.write(text if text.endswith("\n") or not text else f"{text}\n")
        case Mode.JSON:
            sys.stdout.write(data.dumps(value()))
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
    mode: Mode,
    log: Mapping[Path, Mark],
    message: tuple[str, tuple[str, ...]] | None = None,
    root: Path | None = None,
) -> int:
    """Run the check and print the message, the report and the changed files.

    `init`, `update` and `add` run the check with `--write` at their end and give their
    message and hints (§000066, §000067, §000068).

    Args:
        write: True to write the index first.
        mode: The form of the output.
        log: The changes of the command.
        message: The message and the hints of the command before the check, or None.
        root: The root of the project, or None to search from the current folder.

    Returns:
        The exit code: 1 when the check finds errors.
    """
    project = Project.open(root)
    count, errors = run(project, write=write)
    changed = lines(log, project.root)
    head = () if message is None else (_lines(*message),)
    checked = data.report(count, tuple(errors))
    _emit(
        mode,
        lambda: (
            "".join(f"{h}\n" for h in head)
            + "".join(f"{e}\n" for e in errors)
            + f"{count} specs, {len(errors)} errors\n"
            + _raw_changes(changed)
        ),
        lambda: Group(*(done(h) for h in head), report(count, tuple(errors)), file_list(changed)),
        lambda: (
            {**checked, "changed": data.changed(changed)}
            if message is None
            else dict(data.result(message[0], message[1], checked, changed))
        ),
    )
    return 1 if errors else 0


def _message(mode: Mode, text: str, log: Mapping[Path, Mark], root: Path) -> int:
    """Print the message of a command that changes files, and the changed files.

    Args:
        mode: The form of the output.
        text: The message.
        log: The changes of the command.
        root: The root of the project.

    Returns:
        The exit code 0.
    """
    changed = lines(log, root)
    return _emit(
        mode,
        lambda: f"{text}\n{_raw_changes(changed)}",
        lambda: Group(done(text), file_list(changed)),
        lambda: dict(data.result(text, (), None, changed)),
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
        return _dispatch(args, _mode(args), log)


def _dispatch(args: argparse.Namespace, mode: Mode, log: Mapping[Path, Mark]) -> int:
    """Run one command.

    Args:
        args: The parsed command line.
        mode: The form of the output.
        log: The changes of the command, filled while it runs.

    Returns:
        The exit code.
    """
    command: str = args.command
    match command:
        case "check":
            return _check(bool(args.write), mode, log)
        case "init":
            project = init(Path(args.dir), args.forge)
            hints = (
                *init_flake(project.root, project.config.upstream.get(KIT_REPO) or ""),
                *claude_import(project.root),
            )
            text = f"installed the kit in {project.root}"
            return _check(True, mode, log, (text, hints), project.root)
        case "update":
            target = _update_target(list(args.args))
            project = Project.open()
            commit, ran = update(project, *target)
            hints = (
                *(f"migrated: {d}" for d in ran),
                *(update_flake(project.root, commit) if target[0] == KIT_REPO else ()),
            )
            return _check(True, mode, log, (f"updated to {commit}", hints))
        case "add":
            project = Project.open()
            commit, ran = add(project, args.repo, args.ref, tuple(args.include))
            return _check(
                True, mode, log, (f"added at {commit}", tuple(f"migrated: {d}" for d in ran))
            )
        case "new":
            project = Project.open()
            path = new(
                project, args.kind, args.path, args.name, args.title, args.owner, tuple(args.scope)
            )
            return _message(mode, str(path), log, project.root)
        case "resolve":
            project = Project.open()
            spec = queries.find(project, args.id)
            return _emit(
                mode,
                lambda: spec.long,
                lambda: Text(spec.long, style="bold cyan"),
                lambda: data.rule(project, spec),
            )
        case "show":
            project = Project.open()
            spec = queries.find(project, args.id)
            text = spec.path.read_text(encoding="utf-8")
            return _emit(
                mode, lambda: text, lambda: spec_text(text), lambda: data.spec_text(project, spec)
            )
        case "list":
            project = Project.open()
            specs = queries.rules(project, args.kind)
            return _emit(
                mode,
                lambda: queries.listing(project, args.kind),
                lambda: table(specs),
                lambda: [data.rule(project, s) for s in specs],
            )
        case "search":
            project = Project.open()
            found = queries.matches(project, args.text)
            return _emit(
                mode,
                lambda: queries.search(project, args.text),
                lambda: table(found),
                lambda: [data.rule(project, s) for s in found],
            )
        case "mcp":
            return serve()
        case _:
            raise KitError(f"unknown command {command!r}")


def main() -> None:
    """Run the command line and exit with its code.

    A command that stops prints `specs: <error>` to stderr, or with `--json` the object
    `{"error": "<error>"}` to stdout (§000080). The exit code is then 1.
    """
    args = parser().parse_args()
    try:
        sys.exit(dispatch(args))
    except (KitError, NewError, ConfigError, queries.QueryError, OSError) as error:
        match _mode(args):
            case Mode.JSON:
                sys.stdout.write(data.dumps({"error": str(error)}))
                sys.exit(1)
            case _:
                sys.exit(f"specs: {error}")
