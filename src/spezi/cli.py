"""The command `spezi`: check and manage the specs of a project.

Usage:
    spezi check
    spezi install
    spezi init [<dir>] [--forge github|gitlab|codeberg] [--yes]
    spezi update [<repo> [<ref>]] [--yes]
    spezi add [<repo> [<ref>]] [--include <folder>]... [--yes]
    spezi configure [<key> <value>] [--yes]
    spezi remove <repo>
    spezi setup-ide zed|code [--yes]
    spezi new <kind> <area>/<topic> <name> "<title>" --scope <path>... [--owner <login>]
    spezi resolve <id>
    spezi show <id>
    spezi list [<kind>]
    spezi search <text>
    spezi mcp
    spezi lsp

Each command except `mcp` and `lsp` takes `--raw` or `--json`. On a terminal, `init`, `add`,
`update` and `configure` ask questions; `--yes` takes the proposals instead (§000085).
"""

from __future__ import annotations

import argparse
import io
import os
import sys
from collections.abc import Callable, Mapping
from enum import Enum, auto
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, NoReturn, override

from rich.console import Console, Group, RenderableType
from rich.style import StyleType
from rich.text import Text
from rich_argparse import RichHelpFormatter

from spezi import data, ide, lsp, queries
from spezi.ask import Ask, Cancelled, Stop, asker
from spezi.changes import Mark, lines, recording
from spezi.check import run
from spezi.configure import configure, set_value
from spezi.devshell import init_flake, update_flake
from spezi.install import install
from spezi.kit import KitError, add, init, offer_lines, remove, update
from spezi.mcp_server import serve
from spezi.new import NewError, new
from spezi.project import KIT_REPO, ConfigError, Project
from spezi.view import console, done, file_list, report, spec_text, table

if TYPE_CHECKING:
    from _typeshed import SupportsWrite


class _Help(RichHelpFormatter):
    """The help in the colors of the other output, with the words of argparse (§000076)."""

    styles: ClassVar[dict[str, StyleType]] = {
        **RichHelpFormatter.styles,
        "argparse.prog": "bold cyan",
        "argparse.args": "bold cyan",
        "argparse.groups": "bold",
        "argparse.metavar": "cyan",
    }
    group_name_formatter: ClassVar[Callable[[str], str]] = str
    help_markup: ClassVar[bool] = False
    text_markup: ClassVar[bool] = False


def _colored(stream: SupportsWrite[str]) -> bool:
    """Tell if the help on a stream has color (§000076).

    Args:
        stream: The stream of the help.

    Returns:
        True when the stream is a terminal and `NO_COLOR` is not set.
    """
    match stream:
        case io.TextIOBase():
            return stream.isatty() and "NO_COLOR" not in os.environ
        case _:
            return False


class UsageError(Exception):
    """The command line has a wrong argument."""


class _Parser(argparse.ArgumentParser):
    """The parser of the command line.

    It colors its help and its usage only on a terminal (§000076). It stops with
    `{"error": ...}` when the command line has `--json` (§000080).
    """

    @override
    def error(self, message: str) -> NoReturn:
        """Stop for a wrong argument.

        Args:
            message: The error of argparse.

        Raises:
            UsageError: The command line has `--json`.
        """
        match "--json" in sys.argv[1:]:
            case True:
                raise UsageError(message)
            case False:
                super().error(message)

    @override
    def _get_formatter(self) -> argparse.HelpFormatter:
        """Return the formatter, with color for each stream.

        Returns:
            The formatter.
        """
        return _Help(prog=self.prog, console=Console(force_terminal=True))

    @override
    def _print_message(self, message: str, file: SupportsWrite[str] | None = None) -> None:
        """Write a message, plain when its stream must have no color.

        Args:
            message: The message, with color.
            file: The stream, or None for stderr.
        """
        stream = file or sys.stderr
        super()._print_message(
            message if _colored(stream) else Text.from_ansi(message).plain, stream
        )


def parser() -> argparse.ArgumentParser:
    """Return the parser of the command line."""
    root = _Parser(prog="spezi", description="Check and manage the specs of a project.")
    commands = root.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="check the specs; change no file")
    commands.add_parser(
        "install", help="load the copies, write missing files and the index, then check"
    )
    start = commands.add_parser("init", help="install the kit in a project")
    start.add_argument("dir", nargs="?", default=".")
    start.add_argument("--forge", choices=("github", "gitlab", "codeberg"))
    renew = commands.add_parser("update", help="resolve the refs again and replace the copies")
    renew.add_argument("repo", nargs="?", help="a repository, or kit; without it each one")
    renew.add_argument("ref", nargs="?", help="a new tag, branch or commit")
    more = commands.add_parser("add", help="add the copy of a repository")
    more.add_argument("repo", nargs="?", help="the repository; without it the command asks")
    more.add_argument("ref", nargs="?", help="a tag, branch or commit; else the newest tag")
    more.add_argument("--include", action="append", default=[], metavar="folder")
    setting = commands.add_parser("configure", help="change spezi.toml, then install")
    setting.add_argument("key", nargs="?", help="for example features.mcp; without it a menu")
    setting.add_argument("value", nargs="?", help="for example false, 25, origin/main or src,lib")
    commands.add_parser("remove", help="remove the copy of a repository").add_argument("repo")
    commands.add_parser(
        "setup-ide", help="write the extension of the language server for an editor"
    ).add_argument("editor", choices=("zed", "code"))
    for name in ("init", "update", "add", "configure", "setup-ide"):
        commands.choices[name].add_argument(
            "-y",
            "--yes",
            "--non-interactive",
            dest="yes",
            action="store_true",
            help="ask nothing; take the proposals",
        )
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
        if name not in ("mcp", "lsp"):
            form = sub.add_mutually_exclusive_group()
            form.add_argument("--raw", action="store_true", help="print plain text")
            form.add_argument("--json", action="store_true", help="print the data as JSON")
    commands.add_parser("mcp", help="run the MCP server on stdin and stdout")
    commands.add_parser("lsp", help="run the language server on stdin and stdout")
    return root


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

    `install` writes the index and `AGENTS.md` first. `init`, `update` and `add` end with
    `install` and give their message and hints (§000066, §000067, §000068, §000083). The changed
    files come before the report, so that the report is at the end (§000077).

    Args:
        write: True to write the index and `AGENTS.md` first.
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
            + _raw_changes(changed)
            + "".join(f"{e}\n" for e in errors)
            + f"{count} specs, {len(errors)} errors\n"
        ),
        lambda: Group(*(done(h) for h in head), file_list(changed), report(count, tuple(errors))),
        lambda: (
            {**checked, "changed": data.changed(changed)}
            if message is None
            else dict(data.result(message[0], message[1], checked, changed))
        ),
    )
    return 1 if errors else 0


def _message(
    mode: Mode, text: str, log: Mapping[Path, Mark], root: Path, hints: tuple[str, ...] = ()
) -> int:
    """Print the message of a command that changes files, its hints, and the changed files.

    Args:
        mode: The form of the output.
        text: The message.
        log: The changes of the command.
        root: The root of the project.
        hints: The hints.

    Returns:
        The exit code 0.
    """
    changed = lines(log, root)
    return _emit(
        mode,
        lambda: f"{_lines(text, hints)}\n{_raw_changes(changed)}",
        lambda: Group(done(_lines(text, hints)), file_list(changed)),
        lambda: dict(data.result(text, hints, None, changed)),
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


def _ask(args: argparse.Namespace, mode: Mode) -> Ask:
    """Return the questions on a terminal, else the proposals (§000085).

    Args:
        args: The parsed command line.
        mode: The form of the output.

    Returns:
        The questions, or the proposals with `--yes`, with `--json` or without a terminal.
    """
    return asker(yes=bool(getattr(args, "yes", False)), json=mode is Mode.JSON)


def _configure(project: Project, args: argparse.Namespace, mode: Mode) -> str:
    """Change `spezi.toml` with the menu or with one key and its value (§000086).

    Args:
        project: The project.
        args: The parsed command line.
        mode: The form of the output.

    Returns:
        The message.

    Raises:
        KitError: Only a key without a value, or no terminal for the menu.
    """
    ask = _ask(args, mode)
    match args.key, args.value:
        case str() as key, str() as value:
            return set_value(project, key, value)
        case str(), None:
            raise KitError("usage: spezi configure [<key> <value>]")
        case _ if not ask.interactive:
            raise KitError("spezi configure needs a terminal, or a key and a value")
        case _:
            return "saved spezi.toml" if configure(project, ask) else "spezi.toml did not change"


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
            return _check(False, mode, log)
        case "install":
            project = Project.open()
            hints = install(project)
            return _check(True, mode, log, ("installed", hints), project.root)
        case "init":
            ask = _ask(args, mode)
            project, commit = init(Path(args.dir), args.forge, ask)
            offer_lines(project.root, project.config.features, ask)
            hints = (*init_flake(project.root, commit, project.config.features), *install(project))
            text = f"installed the kit in {project.root}"
            return _check(True, mode, log, (text, hints), project.root)
        case "update":
            project = Project.open()
            done, ran = update(project, args.repo, args.ref, _ask(args, mode))
            kit = dict(done).get(KIT_REPO)
            hints = (
                *(f"migrated: {d}" for d in ran),
                *(update_flake(project.root, kit) if kit and project.config.on("flake") else ()),
                *(ide.refresh(Project.open(project.root)) if kit else ()),
                *install(Project.open(project.root)),
            )
            text = "; ".join(f"updated {repo} to {commit}" for repo, commit in done)
            return _check(True, mode, log, (text, hints), project.root)
        case "add":
            project = Project.open()
            commit, ran = add(project, args.repo, args.ref, tuple(args.include), _ask(args, mode))
            hints = (*(f"migrated: {d}" for d in ran), *install(Project.open(project.root)))
            return _check(True, mode, log, (f"added at {commit}", hints), project.root)
        case "configure":
            project = Project.open()
            text = _configure(project, args, mode)
            hints = install(Project.open(project.root))
            return _check(True, mode, log, (text, hints), project.root)
        case "remove":
            project = Project.open()
            text = f"removed {remove(project, args.repo)}"
            hints = install(Project.open(project.root))
            return _check(True, mode, log, (text, hints), project.root)
        case "setup-ide":
            project = Project.open()
            text, hints = ide.setup(project, args.editor, _ask(args, mode))
            return _message(mode, text, log, project.root, hints)
        case "new":
            project = Project.open()
            path = new(
                project, args.kind, args.path, args.name, args.title, args.owner, tuple(args.scope)
            )
            return _message(mode, path.relative_to(project.root).as_posix(), log, project.root)
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
        case "lsp":
            return lsp.serve()
        case _:
            raise KitError(f"unknown command {command!r}")


def main() -> None:
    """Run the command line and exit with its code.

    A command that stops prints `specs: <error>` to stderr, or with `--json` the object
    `{"error": "<error>"}` to stdout (§000080). The exit code is then 1.
    """
    try:
        args = parser().parse_args()
    except UsageError as error:
        sys.stdout.write(data.dumps({"error": str(error)}))
        sys.exit(1)
    try:
        sys.exit(dispatch(args))
    except (
        KitError,
        NewError,
        ConfigError,
        queries.QueryError,
        Cancelled,
        Stop,
        OSError,
    ) as error:
        match _mode(args):
            case Mode.JSON:
                sys.stdout.write(data.dumps({"error": str(error)}))
                sys.exit(1)
            case _:
                sys.exit(f"spezi: {error}")
