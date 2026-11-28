"""`spezi lsp`: the language server of the specs on stdin and stdout (spec 000088).

The server shows the errors of `spezi check` at their line. It checks the whole project when
the client starts it and after each save, and the open file 300 ms after its last change, with
the text in the editor. On a reference to a rule it gives a hover with the rule and a
definition. It writes no file.
"""

from __future__ import annotations

import asyncio
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path

from lsprotocol import types
from pygls.lsp.server import LanguageServer
from pygls.uris import to_fs_path

from spezi.check import run
from spezi.project import (
    CONFIG_NAME,
    NUMBER,
    PREFIXES,
    REPO,
    ConfigError,
    Project,
    Spec,
    editing,
)
from spezi.refs import LOOSE_ITEM, items, markdown_files

DELAY = 0.3
LOCATED = re.compile(r"^(?P<file>[^\s:][^:]*?)(?::(?P<line>[0-9]+))?: (?P<text>.+)$")
RULE_ID = rf"(?:{REPO}:)?(?:(?:{PREFIXES})/[a-z0-9-]+/[a-z0-9-]+/)?{NUMBER}"
IN_FRONT_MATTER = re.compile(rf"(?<![\w/.:-])({RULE_ID})(?![0-9])")

type Found = Mapping[Path, tuple[types.Diagnostic, ...]]


@dataclass(slots=True)
class State:
    """What the server keeps between two requests.

    Attributes:
        published: The files that have diagnostics in the client.
        pending: The waiting check of each changed file by URI.
    """

    published: frozenset[Path] = frozenset()
    pending: dict[str, asyncio.Task[None]] = field(default_factory=dict[str, "asyncio.Task[None]"])


server = LanguageServer("spezi", "0.1.0")
state = State()


def _diagnostic(line: int, text: str) -> types.Diagnostic:
    """Return the diagnostic of one error.

    Args:
        line: The line of the error, from 1.
        text: The text of the error.

    Returns:
        The diagnostic over the whole line.
    """
    return types.Diagnostic(
        range=types.Range(
            start=types.Position(line=line - 1, character=0),
            end=types.Position(line=line, character=0),
        ),
        message=text,
        severity=types.DiagnosticSeverity.Error,
        source="spezi",
    )


def _place(root: Path, error: str) -> tuple[Path, types.Diagnostic]:
    """Return the file and the diagnostic of one error.

    Args:
        root: The root of the project.
        error: The error line of the check.

    Returns:
        The file of the error, or `spezi.toml` for a folder, a missing file or an error without
        a file, and the diagnostic.
    """
    found = LOCATED.match(error)
    return (
        ((root / found["file"]).resolve(), _diagnostic(int(found["line"] or 1), found["text"]))
        if found and (root / found["file"]).is_file()
        else ((root / CONFIG_NAME).resolve(), _diagnostic(1, error))
    )


def diagnostics(root: Path, errors: Iterable[str]) -> Found:
    """Return the diagnostics of the errors by file.

    Args:
        root: The root of the project.
        errors: The error lines of the check.

    Returns:
        The diagnostics of each file with an error.
    """
    placed = tuple(_place(root, e) for e in errors)
    return {
        path: tuple(d for p, d in placed if p == path)
        for path in dict.fromkeys(p for p, _ in placed)
    }


def check(root: Path, texts: Mapping[Path, str]) -> tuple[str, ...]:
    """Run the check of the project without a write.

    Args:
        root: The root of the project.
        texts: The text of each file that the editor changed, by absolute path.

    Returns:
        The error lines, or the error of `spezi.toml` when it is not valid.
    """
    try:
        with editing(texts):
            return run(Project.open(root), write=False)[1]
    except ConfigError as error:
        return (str(error),)


def _root(ls: LanguageServer) -> Path:
    """Return the root of the workspace.

    Args:
        ls: The server.

    Returns:
        The root, or the current folder when the client gave none.
    """
    return Path(ls.workspace.root_path or Path.cwd()).resolve()


def _path(uri: str) -> Path:
    """Return the file of a URI.

    Args:
        uri: The URI.

    Returns:
        The absolute path.
    """
    return Path(to_fs_path(uri) or uri).resolve()


def _publish(ls: LanguageServer, found: Found, paths: Iterable[Path]) -> None:
    """Send the diagnostics of some files to the client, an empty list for a file without one.

    Args:
        ls: The server.
        found: The diagnostics by file.
        paths: The files.
    """
    for path in paths:
        ls.text_document_publish_diagnostics(
            types.PublishDiagnosticsParams(uri=path.as_uri(), diagnostics=list(found.get(path, ())))
        )


def check_project(ls: LanguageServer) -> None:
    """Check the whole project from the disk and replace every diagnostic.

    Args:
        ls: The server.
    """
    root = _root(ls)
    found = diagnostics(root, check(root, {}))
    _publish(ls, found, (*state.published, *(p for p in found if p not in state.published)))
    state.published = frozenset(found)


def check_file(ls: LanguageServer, uri: str) -> None:
    """Check one open file with the text in the editor and replace its diagnostics.

    Args:
        ls: The server.
        uri: The URI of the file.
    """
    root = _root(ls)
    path = _path(uri)
    found = diagnostics(root, check(root, {path: ls.workspace.get_text_document(uri).source}))
    _publish(ls, found, (path,))
    state.published = state.published | {path} if path in found else state.published - {path}


async def _later(ls: LanguageServer, uri: str) -> None:
    """Check one file after the delay.

    Args:
        ls: The server.
        uri: The URI of the file.
    """
    await asyncio.sleep(DELAY)
    check_file(ls, uri)


def _cancel(uri: str) -> None:
    """Stop the waiting check of one file.

    Args:
        uri: The URI of the file.
    """
    match state.pending.pop(uri, None):
        case asyncio.Task() as task:
            task.cancel()
        case _:
            pass


def _kind(project: Project, path: Path) -> str | None:
    """Return the kind of a file that the server serves.

    Args:
        project: The project.
        path: The absolute path of the file.

    Returns:
        `spec` for a Markdown file below `specs/`, `text` for a different Markdown file that git
        tracks or a file of `code_dirs` with a suffix of the code, else None.
    """
    rel = path.relative_to(project.root).as_posix() if path.is_relative_to(project.root) else ""
    spec = path.is_relative_to(project.specs_dir) and path.suffix == ".md"
    code = path.suffix in project.config.code_suffixes and any(
        path.is_relative_to(project.root / d) for d in project.config.code_dirs
    )
    match spec, code or rel in markdown_files(project.root):
        case True, _:
            return "spec"
        case _, True:
            return "text"
        case _:
            return None


def _front_matter_end(lines: list[str]) -> int:
    """Return the line after the front matter.

    Args:
        lines: The lines of the file.

    Returns:
        The line of the second `---`, from 0, or 0 without front matter.
    """
    return (
        next(
            (n for n, line in enumerate(lines[1:], 1) if line == "---"),
            0,
        )
        if lines[:1] == ["---"]
        else 0
    )


def _span(line: int, start: int, end: int) -> types.Range:
    """Return the range of a part of one line.

    Args:
        line: The line, from 0.
        start: The first column, from 0.
        end: The column after the part.

    Returns:
        The range.
    """
    return types.Range(
        start=types.Position(line=line, character=start),
        end=types.Position(line=line, character=end),
    )


def reference(kind: str, text: str, line: int, column: int) -> tuple[str, types.Range] | None:
    """Return the rule ID at a position and the range of the rule ID.

    Args:
        kind: `spec` or `text`, see `_kind`.
        text: The text of the file.
        line: The line, from 0.
        column: The column, from 0.

    Returns:
        The ID and its range: a rule ID in the front matter of a spec, else a rule ID in a
        `(spec ...)` reference. None when there is no reference at the position.
    """
    lines = text.splitlines()
    here = lines[line] if line < len(lines) else ""
    front = kind == "spec" and 0 < line < _front_matter_end(lines)
    found = (
        ((m[1], m.start(1), m.end(1)) for m in IN_FRONT_MATTER.finditer(here))
        if front
        else ((i.text, i.start, i.end) for i in items(here) if LOOSE_ITEM.fullmatch(i.text))
    )
    return next(
        ((ref, _span(line, start, end)) for ref, start, end in found if start <= column <= end),
        None,
    )


def _in_copy(project: Project, path: Path, ref: str) -> str:
    """Return the ID with the repository of the copy that holds the file.

    Args:
        project: The project.
        path: The absolute path of the file.
        ref: The ID.

    Returns:
        The ID. A short ID in a copy gets the repository of the copy.
    """
    repo = next(
        (r for r in project.copies() if path.is_relative_to(project.upstream_dir / r)), None
    )
    return f"{repo}:{ref}" if repo and ":" not in ref else ref


def target(
    ls: LanguageServer, uri: str, position: types.Position
) -> tuple[Spec, types.Range] | None:
    """Return the rule of the reference at a position and the range of the reference.

    Args:
        ls: The server.
        uri: The URI of the file.
        position: The position.

    Returns:
        The spec and the range, or None when there is no reference or no rule.
    """
    path = _path(uri)
    try:
        project = Project.open(_root(ls))
    except ConfigError:
        return None
    kind = _kind(project, path)
    text = ls.workspace.get_text_document(uri).source
    found = reference(kind, text, position.line, position.character) if kind else None
    match found:
        case (ref, span):
            spec = project.find(_in_copy(project, path, ref))
            return (spec, span) if spec else None
        case _:
            return None


def hover_text(spec: Spec) -> str:
    """Return the text of the hover of a rule.

    Args:
        spec: The rule.

    Returns:
        The long form, the status, the title and the text after the front matter, as Markdown.
    """
    return f"`{spec.long}` ({spec.status})\n\n**{spec.title}**\n\n---\n\n{spec.body.strip()}\n"


@server.feature(types.INITIALIZED)
def _initialized(ls: LanguageServer, params: types.InitializedParams) -> None:
    """Check the whole project when the client starts the server.

    Args:
        ls: The server.
        params: The parameters.
    """
    del params
    check_project(ls)


@server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
def _changed(ls: LanguageServer, params: types.DidChangeTextDocumentParams) -> None:
    """Check the changed file 300 ms after its last change.

    Args:
        ls: The server.
        params: The parameters.
    """
    uri = params.text_document.uri
    _cancel(uri)
    state.pending[uri] = asyncio.ensure_future(_later(ls, uri))


@server.feature(types.TEXT_DOCUMENT_DID_SAVE)
def _saved(ls: LanguageServer, params: types.DidSaveTextDocumentParams) -> None:
    """Check the whole project after a save.

    Args:
        ls: The server.
        params: The parameters.
    """
    _cancel(params.text_document.uri)
    check_project(ls)


@server.feature(types.TEXT_DOCUMENT_HOVER)
def _hover(ls: LanguageServer, params: types.HoverParams) -> types.Hover | None:
    """Show the rule of the reference under the cursor.

    Args:
        ls: The server.
        params: The parameters.

    Returns:
        The hover, or None.
    """
    match target(ls, params.text_document.uri, params.position):
        case (spec, span):
            return types.Hover(
                contents=types.MarkupContent(
                    kind=types.MarkupKind.Markdown, value=hover_text(spec)
                ),
                range=span,
            )
        case _:
            return None


def _links(ls: LanguageServer) -> bool:
    """Return whether the client takes a `LocationLink` as the definition.

    Args:
        ls: The server.

    Returns:
        True when the client gives `linkSupport` for the definition.
    """
    document = ls.client_capabilities.text_document
    definition = document.definition if document else None
    return bool(definition and definition.link_support)


@server.feature(types.TEXT_DOCUMENT_DEFINITION)
def _definition(
    ls: LanguageServer, params: types.DefinitionParams
) -> types.Location | list[types.LocationLink] | None:
    """Give the first line of the file of the rule under the cursor.

    Args:
        ls: The server.
        params: The parameters.

    Returns:
        A link with the range of the reference when the client takes links, else the location,
        or None.
    """
    start = types.Position(line=0, character=0)
    top = types.Range(start=start, end=start)
    match target(ls, params.text_document.uri, params.position), _links(ls):
        case (spec, span), True:
            return [
                types.LocationLink(
                    target_uri=spec.path.resolve().as_uri(),
                    target_range=top,
                    target_selection_range=top,
                    origin_selection_range=span,
                )
            ]
        case (spec, _), False:
            return types.Location(uri=spec.path.resolve().as_uri(), range=top)
        case _:
            return None


def serve() -> int:
    """Run the server on stdin and stdout.

    Returns:
        The exit code 0 after the client closed the connection.
    """
    server.start_io()
    return 0
