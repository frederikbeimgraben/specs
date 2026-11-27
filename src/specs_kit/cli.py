"""The command `specs`: check and manage the specs of a project.

Usage:
    specs check [--write]
    specs init [<dir>] [--forge github|gitlab|codeberg]
    specs update [<ref>]
    specs update <repo> <ref>
    specs add <repo> <ref> [--include <folder>]...
    specs new <kind> <area>/<topic> <name> "<title>" [--owner <login>]
    specs resolve <id>
    specs show <id>
    specs list
    specs search <text>
    specs mcp
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from specs_kit import queries
from specs_kit.check import run
from specs_kit.kit import KitError, add, init, update
from specs_kit.mcp_server import serve
from specs_kit.new import NewError, new
from specs_kit.project import KIT_REPO, Project


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
    commands.add_parser("resolve", help="print the long form of a rule ID").add_argument("id")
    commands.add_parser("show", help="print the full text of a spec").add_argument("id")
    commands.add_parser("list", help="list every rule")
    commands.add_parser("search", help="list the rules that hold a text").add_argument("text")
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


def _check(write: bool) -> int:
    """Run the check and print the report.

    Args:
        write: True to write the index first.

    Returns:
        The exit code.
    """
    count, errors = run(Project.open(), write=write)
    print("".join(f"{e}\n" for e in errors) + f"{count} specs, {len(errors)} errors")
    return 1 if errors else 0


def _print(text: str) -> int:
    """Print a text without an extra newline.

    Args:
        text: The text.

    Returns:
        The exit code 0.
    """
    sys.stdout.write(text if text.endswith("\n") or not text else f"{text}\n")
    return 0


def dispatch(args: argparse.Namespace) -> int:
    """Run one command.

    Args:
        args: The parsed command line.

    Returns:
        The exit code.
    """
    command: str = args.command
    match command:
        case "check":
            return _check(bool(args.write))
        case "init":
            return _print(f"installed the kit in {init(Path(args.dir), args.forge).root}")
        case "update":
            return _print(f"updated to {update(Project.open(), *_update_target(list(args.args)))}")
        case "add":
            return _print(
                f"added at {add(Project.open(), args.repo, args.ref, tuple(args.include))}"
            )
        case "new":
            return _print(
                str(new(Project.open(), args.kind, args.path, args.name, args.title, args.owner))
            )
        case "resolve":
            return _print(queries.resolve(Project.open(), args.id))
        case "show":
            return _print(queries.show(Project.open(), args.id))
        case "list":
            return _print(queries.listing(Project.open()))
        case "search":
            return _print(queries.search(Project.open(), args.text))
        case "mcp":
            return serve()
        case _:
            raise KitError(f"unknown command {command!r}")


def main() -> None:
    """Run the command line and exit with its code."""
    try:
        sys.exit(dispatch(parser().parse_args()))
    except (KitError, NewError, queries.QueryError) as error:
        sys.exit(f"specs: {error}")
