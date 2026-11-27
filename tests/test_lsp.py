"""Tests of `specs lsp`, the language server (§000088)."""

from __future__ import annotations

import asyncio
import sys
from collections.abc import AsyncGenerator, Callable, Coroutine
from contextlib import asynccontextmanager
from pathlib import Path

from conftest import Kit, write_rule
from lsprotocol import types
from pygls.lsp.client import LanguageClient

type Seen = dict[str, list[types.Diagnostic]]


@asynccontextmanager
async def _session(kit: Kit, project: Path) -> AsyncGenerator[tuple[LanguageClient, Seen]]:
    """Start the server in the project and initialize it.

    Args:
        kit: The kit.
        project: The root of the project.

    Yields:
        The client and the last diagnostics of each URI.
    """
    client = LanguageClient("test", "1")
    seen: Seen = {}

    @client.feature(types.TEXT_DOCUMENT_PUBLISH_DIAGNOSTICS)
    def _published(params: types.PublishDiagnosticsParams) -> None:
        seen[params.uri] = list(params.diagnostics)

    await client.start_io(sys.executable, "-m", "specs_kit", "lsp", cwd=project, env=dict(kit.env))
    await client.initialize_async(
        types.InitializeParams(
            capabilities=types.ClientCapabilities(), root_uri=project.resolve().as_uri()
        )
    )
    client.initialized(types.InitializedParams())
    try:
        yield client, seen
    finally:
        await client.shutdown_async(None)
        client.exit(None)
        await client.stop()


async def _until[T](found: Callable[[], T | None]) -> T:
    """Wait until a value is there.

    Args:
        found: Returns the value, or None while it is missing.

    Returns:
        The value.
    """
    for _ in range(400):
        value = found()
        if value is not None:
            return value
        await asyncio.sleep(0.05)
    raise AssertionError("no value after 20 s")


def _run(test: Coroutine[None, None, None]) -> None:
    """Run one async test.

    Args:
        test: The test.
    """
    asyncio.run(test)


def _rule(project: Path, number: str, name: str, text: str) -> Path:
    """Write one style rule to the project.

    Args:
        project: The root of the project.
        number: The number.
        name: The name of the file.
        text: The rule text.

    Returns:
        The file.
    """
    (project / "src").mkdir(exist_ok=True)
    return write_rule(project, "style/code/names", number, name, f"Rule {number}", "style", text)


def _open(client: LanguageClient, path: Path) -> str:
    """Open a file in the server.

    Args:
        client: The client.
        path: The file.

    Returns:
        The URI of the file.
    """
    uri = path.resolve().as_uri()
    client.text_document_did_open(
        types.DidOpenTextDocumentParams(
            text_document=types.TextDocumentItem(
                uri=uri, language_id="markdown", version=1, text=path.read_text(encoding="utf-8")
            )
        )
    )
    return uri


def test_the_server_shows_the_errors_of_the_project(kit: Kit, project: Path) -> None:
    """At the start the server shows each error at its line, and a save removes a fixed one."""
    path = _rule(project, "000100", "short-names", "A name must be short.")
    assert kit.run(project, "install", "--raw").code == 0
    path.write_text(
        path.read_text(encoding="utf-8").replace("updated: 2026-11-27", "updated: today"),
        encoding="utf-8",
    )
    uri = path.resolve().as_uri()

    async def test() -> None:
        async with _session(kit, project) as (client, seen):
            first = await _until(lambda: seen.get(uri) or None)
            assert [(d.range.start.line, d.severity) for d in first] == [
                (6, types.DiagnosticSeverity.Error)
            ]
            assert "updated must be YYYY-MM-DD" in first[0].message
            path.write_text(
                path.read_text(encoding="utf-8").replace("updated: today", "updated: 2026-11-27"),
                encoding="utf-8",
            )
            client.text_document_did_save(
                types.DidSaveTextDocumentParams(text_document=types.TextDocumentIdentifier(uri=uri))
            )
            await _until(lambda: True if seen.get(uri) == [] else None)

    _run(test())


def test_the_server_checks_the_text_while_it_changes(kit: Kit, project: Path) -> None:
    """A change of an open file shows the errors of the text in the editor."""
    path = _rule(project, "000100", "short-names", "A name must be short.")
    assert kit.run(project, "install", "--raw").code == 0
    changed = path.read_text(encoding="utf-8").replace("short.", "short, see §000999.")

    async def test() -> None:
        async with _session(kit, project) as (client, seen):
            uri = _open(client, path)
            client.text_document_did_change(
                types.DidChangeTextDocumentParams(
                    text_document=types.VersionedTextDocumentIdentifier(uri=uri, version=2),
                    content_changes=[types.TextDocumentContentChangeWholeDocument(text=changed)],
                )
            )
            found = await _until(lambda: seen.get(uri) or None)
            assert [(d.range.start.line, d.message) for d in found] == [
                (14, "a spec refers to a rule without § (000017): §000999")
            ]

    _run(test())


def _referring(kit: Kit, project: Path) -> tuple[Path, Path]:
    """Write a rule and a second rule that refers to it, then install.

    Args:
        kit: The kit.
        project: The root of the project.

    Returns:
        The rule and the rule that refers to it.
    """
    rule = _rule(project, "000100", "short-names", "A name must be short.")
    other = _rule(project, "000101", "long-names", "A name must not be long, as 000100 says.")
    assert kit.run(project, "install", "--raw").code == 0
    return rule, other


def test_the_hover_shows_the_rule(kit: Kit, project: Path) -> None:
    """The hover over a reference shows the long form, the title, the status and the text."""
    _, other = _referring(kit, project)

    async def test() -> None:
        async with _session(kit, project) as (client, _):
            uri = _open(client, other)
            hover = await client.text_document_hover_async(
                types.HoverParams(
                    text_document=types.TextDocumentIdentifier(uri=uri),
                    position=types.Position(line=14, character=31),
                )
            )
            assert hover is not None
            assert isinstance(hover.contents, types.MarkupContent)
            text = hover.contents.value
            assert "S/code/names/000100" in text
            assert "Rule 000100" in text
            assert "approved" in text
            assert "A name must be short." in text

    _run(test())


def test_the_definition_opens_the_spec(kit: Kit, project: Path) -> None:
    """The definition of a reference is the first line of the file of the rule."""
    rule, other = _referring(kit, project)

    async def test() -> None:
        async with _session(kit, project) as (client, _):
            uri = _open(client, other)
            found = await client.text_document_definition_async(
                types.DefinitionParams(
                    text_document=types.TextDocumentIdentifier(uri=uri),
                    position=types.Position(line=14, character=31),
                )
            )
            assert isinstance(found, types.Location)
            assert found.uri == rule.resolve().as_uri()
            assert found.range.start.line == 0

    _run(test())


def test_the_server_writes_no_file(kit: Kit, project: Path) -> None:
    """The server shows a stale index as an error and does not write it."""
    _rule(project, "000100", "short-names", "A name must be short.")
    index = project / "specs" / "README.md"
    before = index.read_text(encoding="utf-8")
    uri = index.resolve().as_uri()

    async def test() -> None:
        async with _session(kit, project) as (_, seen):
            found = await _until(lambda: seen.get(uri) or None)
            assert "the index is not current" in found[0].message

    _run(test())
    assert index.read_text(encoding="utf-8") == before
