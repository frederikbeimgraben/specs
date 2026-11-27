"""The MCP server `specs` in stdio mode. Only the tool `new` writes."""

from __future__ import annotations

from mcp.server.mcpserver import MCPServer

from specs_kit import queries
from specs_kit.changes import lines, recording
from specs_kit.new import new as new_spec
from specs_kit.project import Project

server = MCPServer("specs")


@server.tool()
def check() -> str:
    """Check the specs of the project and return the report. The tool writes nothing."""
    return queries.check(Project.open())[1]


@server.tool()
def resolve(ref: str) -> str:
    """Return the long form of a rule ID, for example 000012 or github.com/o/r:000012.

    Args:
        ref: The short or the long ID.
    """
    return queries.resolve(Project.open(), ref)


@server.tool()
def show(ref: str) -> str:
    """Return the full text of a spec.

    Args:
        ref: The short or the long ID.
    """
    return queries.show(Project.open(), ref)


@server.tool(name="list")
def list_specs() -> str:
    """Return one line per rule of the project and of the copies: kind, ID, status, title."""
    return queries.listing(Project.open())


@server.tool()
def search(text: str) -> str:
    """Return the rules whose title or text holds a text, without case.

    Args:
        text: The text to find.
    """
    return queries.search(Project.open(), text)


@server.tool()
def new(
    kind: str, path: str, name: str, title: str, scope: list[str], owner: str | None = None
) -> str:
    """Create a new spec from its template and return the created file as `A <path>`.

    Args:
        kind: The kind name or letter, for example convention or C.
        path: The area and the topic, as <area>/<topic>.
        name: The short name of the file, in kebab case.
        title: The title of the rule.
        scope: The paths of the rule, from the root of the project. At least one.
        owner: The login of the owner. Without it, git config <forge>.user.
    """
    project = Project.open()
    with recording() as log:
        new_spec(project, kind, path, name, title, owner, tuple(scope))
        return "".join(f"{mark} {file}\n" for mark, file in lines(log, project.root))


def serve() -> int:
    """Run the server on stdin and stdout.

    Returns:
        The exit code 0 after the client closed the connection.
    """
    server.run("stdio")
    return 0
