"""The MCP server `specs` in stdio mode. Only `install`, `new`, `configure` and `remove` write."""

from __future__ import annotations

from mcp.server.mcpserver import MCPServer

from specs_kit import queries
from specs_kit.changes import lines, recording
from specs_kit.configure import set_value
from specs_kit.install import install as install_project
from specs_kit.kit import remove as remove_repo
from specs_kit.new import new as new_spec
from specs_kit.project import Project

server = MCPServer("specs")


@server.tool()
def check() -> str:
    """Check the specs of the project and return the report. The tool writes nothing."""
    return queries.check(Project.open())[1]


def _installed(project: Project, head: tuple[str, ...]) -> str:
    """Run `specs install` and return the messages, the hints, the report and the changed files.

    Args:
        project: The project.
        head: The messages before the hints.

    Returns:
        The text.
    """
    hints = install_project(Project.open(project.root))
    _, report = queries.check(Project.open(project.root), write=True)
    return "".join(f"{h}\n" for h in (*head, *hints)) + report


@server.tool()
def install() -> str:
    """Load the copies, write each missing file, the index and AGENTS.md, then check.

    Returns the hints, the report of the check and the changed files as `<mark> <path>` lines.
    """
    project = Project.open()
    with recording() as log:
        text = _installed(project, ())
        return text + "".join(f"{mark} {file}\n" for mark, file in lines(log, project.root))


@server.tool()
def configure(key: str, value: str) -> str:
    """Set one key of specs.toml, then run install. Returns the report and the changed files.

    Args:
        key: forge, base_ref, code_dirs, code_suffixes, max_elements or features.<switch>.
        value: The plain value, for example false, 25, origin/main or src,lib.
    """
    project = Project.open()
    with recording() as log:
        text = _installed(project, (set_value(project, key, value),))
        return text + "".join(f"{mark} {file}\n" for mark, file in lines(log, project.root))


@server.tool()
def remove(repo: str) -> str:
    """Remove the copy of a repository from specs.toml, specs.lock and specs/.upstream/.

    Args:
        repo: The full name of the repository. The kit cannot be removed.
    """
    project = Project.open()
    with recording() as log:
        text = _installed(project, (f"removed {remove_repo(project, repo)}",))
        return text + "".join(f"{mark} {file}\n" for mark, file in lines(log, project.root))


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
def list_specs(kind: str | None = None) -> str:
    """Return one line per rule of the project and of the copies: kind, ID, status, title.

    Args:
        kind: Only the rules of this kind, as kind name or kind letter.
    """
    return queries.listing(Project.open(), kind)


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
