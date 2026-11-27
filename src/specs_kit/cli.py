"""The command `specs`: check and manage the specs of a project.

Usage:
    specs check
    specs install
    specs init [<dir>] [--forge github|gitlab|codeberg] [--yes]
    specs update [<repo> [<ref>]] [--yes]
    specs add [<repo> [<ref>]] [--include <folder>]... [--yes]
    specs configure [<key> <value>] [--yes]
    specs remove <repo>
    specs new <kind> <area>/<topic> <name> "<title>" --scope <path>... [--owner <login>]
    specs resolve <id>
    specs show <id>
    specs list [<kind>]
    specs search <text>
    specs mcp

Each command except `mcp` takes `--raw` or `--json`. On a terminal, `init`, `add`, `update` and
`configure` ask questions; `--yes` takes the proposals instead (§000085).
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
from specs_kit.ask import Ask, Cancelled, Stop, asker
from specs_kit.changes import Mark, lines, recording
from specs_kit.check import run
from specs_kit.configure import configure, set_value
from specs_kit.devshell import init_flake, update_flake
from specs_kit.install import install
from specs_kit.kit import KitError, add, init, offer_lines, remove, update
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
    setting = commands.add_parser("configure", help="change specs.toml, then install")
    setting.add_argument("key", nargs="?", help="for example features.mcp; without it a menu")
    setting.add_argument("value", nargs="?", help="for example false, 25, origin/main or src,lib")
    commands.add_parser("remove", help="remove the copy of a repository").add_argument("repo")
    for name in ("init", "update", "add", "configure"):
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
        if name != "mcp":
            form = sub.add_mutually_exclusive_group()
            form.add_argument("--raw", action="store_true", help="print plain text")
            form.add_argument("--json", action="store_true", help="print the data as JSON")
    commands.add_parser("mcp", help="run the MCP server on stdin and stdout")
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
    `install` and give their message and hints (§000066, §000067, §000068, §000083).

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
    """Change `specs.toml` with the menu or with one key and its value (§000086).

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
            raise KitError("usage: specs configure [<key> <value>]")
        case _ if not ask.interactive:
            raise KitError("specs configure needs a terminal, or a key and a value")
        case _:
            return "saved specs.toml" if configure(project, ask) else "specs.toml did not change"


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
                sys.exit(f"specs: {error}")
