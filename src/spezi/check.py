"""Check the specs of a project and write its index.

The check covers the spec conventions: the file name, the place in the tree, the front matter,
the headings, the labels, `must` in the rule text, the paths, `replaces`, unique numbers, the
index and every `§` reference in the code. For a protocol spec it also checks the sections, the
schema file and the examples. For a structure spec it checks the Mermaid block and the element
table. For a decision spec it checks the sections.
"""

from __future__ import annotations

import re
import subprocess
from collections.abc import Iterable, Mapping
from pathlib import Path

from spezi.agents import AGENTS, block, merge
from spezi.changes import write_text
from spezi.context import Context, Errors, where
from spezi.index import index
from spezi.lock import LOCK_NAME, read_lock, tree_hash
from spezi.project import (
    FILE_NAME,
    IN_FORCE,
    KINDS_BY_PREFIX,
    LONG_LOCAL,
    NUMBER,
    PREFIXES,
    REPO,
    SHORT,
    STATUSES,
    Project,
    Spec,
    hidden,
    source,
)
from spezi.sections import DIAGRAMS, SECTION_CHECKS, check_plain, schema_path

KEYS = (
    "id",
    "title",
    "kind",
    "status",
    "owner",
    "updated",
    "replaced_by",
    "replaces",
    "version",
    "media_type",
    "diagram",
    "tests",
    "protocols",
    "structures",
    "implementation",
    "scope",
)
REQUIRED = frozenset({"id", "title", "kind", "status", "owner", "updated", "scope"})
VERSION = re.compile(r"^[1-9][0-9]*$")
MEDIA_TYPE = re.compile(r"^[a-z]+/[a-z0-9.+-]+$")
TEST_ENTRY = re.compile(r"^[^:\s]+:[A-Za-z_][A-Za-z0-9_.]*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LABEL = re.compile(r"^(Reason|Test):", re.MULTILINE)
MUST = re.compile(r"\bmust\b")
CODE_REF = re.compile(rf"§((?:{REPO}:)?{NUMBER})(?![0-9])")
CODE_LONG_REF = re.compile(rf"§((?:{REPO}:)?{LONG_LOCAL})")
SPEC_SECTION_REF = re.compile(rf"§ ?(?:(?:{REPO}:)?(?:{PREFIXES})/[a-z0-9/-]+/)?{NUMBER}\b")
FOREIGN_REF = re.compile(rf"(?<![\w/.-])({REPO}):({NUMBER})\b")
FOREIGN_LONG_REF = re.compile(rf"(?<![\w/.-])({REPO}):({LONG_LOCAL})\b")
INLINE_CODE = re.compile(r"`[^`\n]*`")
QUOTED = re.compile(r"'([^'\n]+)'")
NAMED_REF = re.compile(rf"§[^\s]+|(?<![\w/.-])(?:{REPO}):[A-Za-z0-9/-]+")


def _paths(ctx: Context, spec: Spec, key: str) -> Errors:
    """Return an error for each path of a list key that does not exist.

    Args:
        ctx: The context of the check.
        spec: The spec.
        key: The key of the front matter.

    Returns:
        The errors.
    """
    return tuple(
        f"{where(ctx.project, spec)}: {key} path {p!r} does not exist (000009)"
        for p in spec.entries(key) or ()
        if not (ctx.project.root / p).exists()
    )


def _check_implementation(ctx: Context, spec: Spec) -> Errors:
    """Check `implementation` against the status.

    Args:
        ctx: The context of the check.
        spec: The spec.

    Returns:
        The errors.
    """
    rel = where(ctx.project, spec)
    value = spec.meta.get("implementation")
    match spec.status in IN_FORCE, value:
        case True, "null":
            return ()
        case True, tuple() if value:
            return _paths(ctx, spec, "implementation")
        case True, _:
            return (f"{rel}: implementation must be a list of paths or null (000009)",)
        case False, None:
            return ()
        case False, _:
            return (f"{rel}: implementation goes with status draft or approved only (000009)",)


def _check_meta(ctx: Context, spec: Spec) -> Errors:
    """Check the front matter of one spec.

    Args:
        ctx: The context of the check.
        spec: The spec.

    Returns:
        The errors.
    """
    rel = where(ctx.project, spec)
    order = tuple(k for k in KEYS if k in spec.keys)
    raw_id = source(spec.path).split("\n", 2)[1]
    kind = KINDS_BY_PREFIX.get(spec.prefix)
    tests = spec.entries("tests") or ()
    scope = spec.entries("scope")
    return (
        *(
            (f"{rel}: front matter keys or their order break 000009: {list(spec.keys)}",)
            if spec.keys != order or set(spec.keys) - set(KEYS) or REQUIRED - set(spec.keys)
            else ()
        ),
        *(
            ()
            if raw_id == f'id: "{spec.number}"'
            else (f"{rel}: id must be the quoted number of the file name (000009)",)
        ),
        *(
            ()
            if spec.meta.get("kind") == kind
            else (f"{rel}: kind {spec.meta.get('kind')!r} does not match the folder (000004)",)
        ),
        *(() if spec.status in STATUSES else (f"{rel}: status {spec.status!r} breaks 000010",)),
        *(
            ()
            if DATE.match(str(spec.meta.get("updated")))
            else (f"{rel}: updated must be YYYY-MM-DD (000009)",)
        ),
        *_check_kind_keys(ctx, spec),
        *_check_links(ctx, spec, "protocols", "P", "000032"),
        *_check_links(ctx, spec, "structures", "U", "000039"),
        *(
            f"{rel}: tests entry {entry!r} names no test file (000009)"
            for entry in tests
            if not TEST_ENTRY.match(entry) or not (ctx.project.root / entry.split(":")[0]).is_file()
        ),
        *_check_implementation(ctx, spec),
        *(
            _paths(ctx, spec, "scope")
            if scope
            else (f"{rel}: scope must be a list of paths (000009)",)
        ),
    )


def _check_kind_keys(ctx: Context, spec: Spec) -> Errors:
    """Check the keys that only one kind has: `version`, `media_type` and `diagram`.

    Args:
        ctx: The context of the check.
        spec: The spec.

    Returns:
        The errors.
    """
    rel, meta = where(ctx.project, spec), spec.meta
    pairs = (("version", "P"), ("media_type", "P"), ("diagram", "U"))
    return (
        *(
            f"{rel}: a {KINDS_BY_PREFIX[prefix]} spec must have {key} (000009)"
            for key, prefix in pairs
            if spec.prefix == prefix and key not in meta
        ),
        *(
            f"{rel}: {key} goes with kind {KINDS_BY_PREFIX[prefix]} only (000009)"
            for key, prefix in pairs
            if spec.prefix != prefix and key in meta
        ),
        *(
            (f"{rel}: version must be a whole number from 1 (000030)",)
            if "version" in meta and not VERSION.match(str(meta["version"]))
            else ()
        ),
        *(
            (f"{rel}: media_type {meta['media_type']!r} is no media type (000009)",)
            if "media_type" in meta and not MEDIA_TYPE.match(str(meta["media_type"]))
            else ()
        ),
        *(
            (f"{rel}: diagram must be one of {', '.join(DIAGRAMS)} (000034)",)
            if "diagram" in meta and meta["diagram"] not in DIAGRAMS
            else ()
        ),
    )


def _link_error(ctx: Context, rel: str, key: str, entry: str, prefix: str, rule: str) -> Errors:
    """Check one entry of `protocols` or `structures`.

    Args:
        ctx: The context of the check.
        rel: The path of the spec.
        key: The key of the front matter.
        entry: The short form of the linked spec.
        prefix: The kind letter that the linked spec must have.
        rule: The number of the rule for the message.

    Returns:
        The errors.
    """
    target = ctx.local.get(entry)
    match target:
        case None:
            return (f"{rel}: {key} entry {entry!r} names no spec; use the number ({rule})",)
        case Spec() if target.prefix != prefix:
            return (
                f"{rel}: {key} entry {entry!r} names no {KINDS_BY_PREFIX[prefix]} spec ({rule})",
            )
        case Spec() if target.status not in IN_FORCE:
            return (f"{rel}: {key} entry {entry!r} is not in force ({rule})",)
        case Spec():
            return ()


def _check_links(ctx: Context, spec: Spec, key: str, prefix: str, rule: str) -> Errors:
    """Check a list of linked specs, such as `protocols` or `structures`.

    Args:
        ctx: The context of the check.
        spec: The spec.
        key: The key of the front matter.
        prefix: The kind letter that each linked spec must have.
        rule: The number of the rule for the message.

    Returns:
        The errors.
    """
    rel = where(ctx.project, spec)
    value = spec.entries(key)
    if value is None:
        return ()
    kind_error = (
        (f"{rel}: {key} goes with an F or NF spec only ({rule})",)
        if spec.prefix not in ("F", "NF")
        else ()
    )
    if not value:
        return (*kind_error, f"{rel}: {key} must be a list of spec numbers ({rule})")
    return (
        *kind_error,
        *(e for entry in value for e in _link_error(ctx, rel, key, entry, prefix, rule)),
        *(
            (f"{rel}: {key} lists a spec two times ({rule})",)
            if len(set(value)) != len(value)
            else ()
        ),
    )


def _check_body(ctx: Context, spec: Spec) -> Errors:
    """Check the headings, the labels, `must`, the `§` signs and the foreign references.

    Args:
        ctx: The context of the check.
        spec: The spec.

    Returns:
        The errors.
    """
    rel = where(ctx.project, spec)
    labels = LABEL.findall(spec.body)
    rule_text = LABEL.split(spec.body, maxsplit=1)[0]
    text = INLINE_CODE.sub("", spec.body)
    return (
        *SECTION_CHECKS.get(spec.prefix, check_plain)(ctx, spec),
        *(
            ()
            if labels in ([], ["Reason"], ["Test"], ["Reason", "Test"])
            else (f"{rel}: labels must be Reason, then Test, once each (000015)",)
        ),
        *(
            (f"{rel}: the rule text has no must or must not (000021)",)
            if spec.status in IN_FORCE and not MUST.search(rule_text)
            else ()
        ),
        *(
            f"{rel}: a spec refers to a rule without § (000017): {ref}"
            for ref in SPEC_SECTION_REF.findall(text)
        ),
        *(
            f"{rel}: use the short form {repo}:{rule[-6:]} (000047)"
            for repo, rule in FOREIGN_LONG_REF.findall(text)
        ),
        *(
            e
            for repo, number in FOREIGN_REF.findall(text)
            for e in _foreign_error(rel, f"{repo}:{number}", ctx.foreign)
        ),
    )


def _foreign_error(rel: str, ref: str, foreign: Mapping[str, str]) -> Errors:
    """Check one reference to a rule of a different repository.

    Args:
        rel: Where the reference is.
        ref: The short form of the reference.
        foreign: The status of each rule of the copies.

    Returns:
        The errors.
    """
    match foreign.get(ref):
        case None:
            return (f"{rel}: {ref} names no rule in specs/.upstream/ (000047)",)
        case "replaced":
            return (f"{rel}: {ref} names a rule that a project spec replaces (000049)",)
        case status if status in IN_FORCE:
            return ()
        case _:
            return (f"{rel}: {ref} names a rule that is not in force (000049)",)


def _replaces_entry(ctx: Context, spec: Spec, entry: str, foreign: Mapping[str, str]) -> Errors:
    """Check one entry of `replaces`.

    Args:
        ctx: The context of the check.
        spec: The spec that replaces.
        entry: The short form of the replaced rule.
        foreign: The status of each rule of the copies, before `replaces`.

    Returns:
        The errors.
    """
    rel = where(ctx.project, spec)
    target = ctx.local.get(entry)
    match SHORT.match(entry):
        case None:
            return (f"{rel}: replaces entry {entry!r} is not a short form (000047)",)
        case _ if entry == spec.number:
            return (f"{rel}: a spec must not replace itself (000009)",)
        case m if m.group(1):
            return (
                ()
                if entry in foreign
                else (
                    f"{rel}: replaces entry {entry!r} names no rule in specs/.upstream/ (000047)",
                )
            )
        case _ if target is None:
            return (f"{rel}: replaces entry {entry!r} names no spec (000009)",)
        case _ if target.status != "replaced":
            return (f"{rel}: {entry} must have status replaced (000010)",)
        case _ if spec.number not in (target.entries("replaced_by") or ()):
            return (f"{where(ctx.project, target)}: replaced_by must name {spec.number} (000010)",)
        case _:
            return ()


def _replaced_by_entry(ctx: Context, spec: Spec, entry: str) -> Errors:
    """Check one entry of `replaced_by`.

    Args:
        ctx: The context of the check.
        spec: The replaced spec.
        entry: The number of the spec that replaces it.

    Returns:
        The errors.
    """
    rel = where(ctx.project, spec)
    target = ctx.local.get(entry)
    match target:
        case None:
            return (
                f"{rel}: replaced_by entry {entry!r} names no spec of this repository (000009)",
            )
        case Spec() if (
            spec.number not in (target.entries("replaces") or ()) or target.status not in IN_FORCE
        ):
            return (f"{rel}: {entry} is not in force or does not name it in replaces (000010)",)
        case Spec():
            return ()


def _check_replaces(ctx: Context, specs: tuple[Spec, ...], foreign: Mapping[str, str]) -> Errors:
    """Check `replaces`, `replaced_by` and the status `replaced` (§000009, §000010, §000049).

    Args:
        ctx: The context of the check.
        specs: The specs of the project.
        foreign: The status of each rule of the copies, before `replaces`.

    Returns:
        The errors.
    """
    replacing = tuple(s for s in specs if s.entries("replaces") is not None)
    named = frozenset(
        e for s in replacing if s.status in IN_FORCE for e in s.entries("replaces") or ()
    )
    return (
        *(
            f"{where(ctx.project, s)}: replaces must be a list of rule IDs (000009)"
            for s in replacing
            if not s.entries("replaces")
        ),
        *(
            f"{where(ctx.project, s)}: replaces goes with status draft or approved only (000009)"
            for s in replacing
            if s.status not in IN_FORCE
        ),
        *(
            e
            for s in replacing
            if s.status in IN_FORCE
            for entry in s.entries("replaces") or ()
            for e in _replaces_entry(ctx, s, entry, foreign)
        ),
        *(
            f"{where(ctx.project, s)}: replaced_by goes with status replaced only (000009)"
            for s in specs
            if s.status != "replaced" and s.entries("replaced_by") is not None
        ),
        *(
            f"{where(ctx.project, s)}: status replaced, but no spec in force names it in"
            " replaces (000010)"
            for s in specs
            if s.status == "replaced" and s.number not in named
        ),
        *(
            f"{where(ctx.project, s)}: replaced_by must be a list of rule numbers (000009)"
            for s in specs
            if s.status == "replaced" and s.entries("replaced_by") == ()
        ),
        *(
            e
            for s in specs
            if s.status == "replaced"
            for entry in s.entries("replaced_by") or ()
            for e in _replaced_by_entry(ctx, s, entry)
        ),
    )


def _upstream_errors(project: Project) -> Errors:
    """Check that `spezi.toml` and the copies below `specs/.upstream/` agree (§000048).

    Args:
        project: The project.

    Returns:
        The errors.
    """
    upstream = project.config.upstream
    copies = project.copies()
    return (
        *(
            f"specs/.upstream/{repo}: no repository of this name in spezi.toml (000048)"
            for repo in sorted(copies - set(upstream))
        ),
        *(
            f"spezi.toml: upstream {repo!r} is not <host>/<group>/.../<repo> (000047)"
            for repo in sorted(upstream)
            if not re.fullmatch(REPO, repo)
        ),
        *(
            f"spezi.toml: upstream {repo!r} must have ref (000048)"
            for repo, ref in sorted(upstream.items())
            if ref is None
        ),
        *(
            f"spezi.toml: upstream {repo!r} has no copy in specs/.upstream/; run spezi install"
            " (000048)"
            for repo in sorted(upstream)
            if repo not in copies
        ),
        *(
            e
            for repo, include in sorted(project.config.include.items())
            if include and repo in copies
            for e in _include_errors(project, repo, include)
        ),
    )


def _lock_errors(project: Project) -> Errors:
    """Check that `spezi.lock`, `spezi.toml` and the copies agree (§000082).

    Args:
        project: The project.

    Returns:
        The errors.
    """
    lock = read_lock(project.root)
    upstream = project.config.upstream
    copies = project.copies()
    return (
        *(
            f"{LOCK_NAME}: no entry for {repo!r}; run spezi install (000082)"
            for repo in sorted(upstream)
            if repo not in lock
        ),
        *(
            f"{LOCK_NAME}: {repo!r} is not in spezi.toml; run spezi install (000082)"
            for repo in sorted(set(lock) - set(upstream))
        ),
        *(
            f"{LOCK_NAME}: {repo!r} does not agree with ref or include in spezi.toml;"
            " run spezi install (000082)"
            for repo, entry in sorted(lock.items())
            if repo in upstream
            and (
                entry.ref != upstream[repo]
                or entry.include
                != tuple(sorted({f.strip("/") for f in project.config.include.get(repo, ())}))
            )
        ),
        *(
            f"specs/.upstream/{repo}: the copy does not agree with its hash in {LOCK_NAME};"
            " run spezi install (000048)"
            for repo, entry in sorted(lock.items())
            if repo in copies and tree_hash(project.upstream_dir / repo) != entry.hash
        ),
    )


def _include_errors(project: Project, repo: str, include: tuple[str, ...]) -> Errors:
    """Check that the copy of one repository holds the folders of `include` and nothing else.

    Args:
        project: The project.
        repo: The repository.
        include: The folders of `include` in `spezi.toml`.

    Returns:
        The errors.
    """
    root = project.upstream_dir / repo
    folders = tuple(f.strip("/") for f in include)
    return (
        *(
            f"spezi.toml: include {f!r} of {repo!r} is not in the copy; run spezi install (000048)"
            for f in folders
            if not (root / f).is_dir()
        ),
        *(
            f"specs/.upstream/{repo}/{p.relative_to(root).as_posix()}: not in include of"
            " spezi.toml; run spezi install (000048)"
            for p in sorted(root.rglob("*"))
            if p.is_file()
            and not any(p.relative_to(root).as_posix().startswith(f"{f}/") for f in folders)
        ),
    )


def _code_files(project: Project) -> Iterable[Path]:
    """Return the code files of `code_dirs`.

    Args:
        project: The project.

    Returns:
        The files.
    """
    return (
        path
        for folder in project.config.code_dirs
        for path in sorted((project.root / folder).rglob("*"))
        if path.is_file()
        and path.suffix in project.config.code_suffixes
        and "node_modules" not in path.parts
    )


def _code_ref_error(ctx: Context, rel: str, ref: str) -> Errors:
    """Check one `§` reference in the code.

    Args:
        ctx: The context of the check.
        rel: The path of the code file.
        ref: The short form after `§`.

    Returns:
        The errors.
    """
    return (
        _foreign_error(rel, ref, ctx.foreign)
        if ":" in ref
        else (() if ref in ctx.local else (f"{rel}: §{ref} names no spec (000017)",))
    )


def _code_refs(ctx: Context) -> Errors:
    """Check the `§` references in the code (§000017, §000047).

    Args:
        ctx: The context of the check.

    Returns:
        The errors.
    """
    texts = tuple(
        (p.relative_to(ctx.project.root).as_posix(), source(p, "ignore"))
        for p in _code_files(ctx.project)
    )
    return (
        *(
            f"{rel}: §{ref} must use the short form (000017)"
            for rel, text in texts
            for ref in CODE_LONG_REF.findall(text)
        ),
        *(
            e
            for rel, text in texts
            for ref in CODE_REF.findall(text)
            for e in _code_ref_error(ctx, rel, ref)
        ),
    )


def _git(project: Project, *args: str) -> str | None:
    """Run git in the project and return its output, or None when it fails.

    Args:
        project: The project.
        *args: The arguments of git.

    Returns:
        The output, or None.
    """
    try:
        return subprocess.run(
            ["git", *args], cwd=project.root, capture_output=True, text=True, check=True
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return None


def git_numbers(project: Project, ref: str) -> Mapping[str, str] | None:
    """Return number to spec path of the rules of the project at a git ref (§000013).

    The copies of different repositories keep their own numbers (§000047), so the files below
    a hidden folder of `specs/` do not count, and neither do the schema files.

    Args:
        project: The project.
        ref: The git ref.

    Returns:
        The paths by number, or None when git cannot read the ref.
    """
    out = _git(project, "ls-tree", "-r", "--name-only", ref, "--", "specs")
    return (
        None
        if out is None
        else {
            Path(line).name[:6]: line
            for line in out.splitlines()
            if FILE_NAME.match(Path(line).name) and not hidden(Path(line).relative_to("specs"))
        }
    )


def _base_errors(project: Project, specs: tuple[Spec, ...]) -> Errors:
    """Return the numbers that the base branch gave to a different spec (§000013).

    A number collides when the base branch added it after the branch left the base branch, and
    the working tree has it at a different path. A checkout without the ref checks nothing.

    Args:
        project: The project.
        specs: The specs of the project.

    Returns:
        The errors.
    """
    base_ref = project.config.base_ref
    fork_ref = (_git(project, "merge-base", "HEAD", base_ref) or "").strip()
    base = git_numbers(project, base_ref) if fork_ref else None
    fork = git_numbers(project, fork_ref) if fork_ref else None
    if base is None or fork is None:
        return ()
    return tuple(
        f"{where(project, s)}: number {s.number} is {base[s.number]} on {base_ref}; give the"
        " spec a new number (000013)"
        for s in sorted(specs, key=lambda s: s.number)
        if s.number in base and s.number not in fork and base[s.number] != where(project, s)
    )


def _number_errors(project: Project, specs: tuple[Spec, ...]) -> Errors:
    """Return an error for each number that two specs use (§000013).

    Args:
        project: The project.
        specs: The specs of the project.

    Returns:
        The errors.
    """
    first = {s.number: s for s in reversed(specs)}
    return tuple(
        f"{where(project, s)}: number used by {where(project, first[s.number])} (000013)"
        for s in specs
        if first[s.number] is not s
    )


def _schema_errors(project: Project, specs: tuple[Spec, ...]) -> Errors:
    """Return an error for each schema file that no protocol spec owns (§000028).

    Args:
        project: The project.
        specs: The specs of the project.

    Returns:
        The errors.
    """
    owned = frozenset(schema_path(s.path) for s in specs if s.prefix == "P")
    folder = project.specs_dir / "protocols"
    return tuple(
        f"{p.relative_to(project.root).as_posix()}: no protocol spec owns this schema file (000028)"
        for p in (sorted(folder.rglob("*.json")) if folder.is_dir() else ())
        if p not in owned
    )


def foreign_status(specs: tuple[Spec, ...], upstream: tuple[Spec, ...]) -> Mapping[str, str]:
    """Return the status of each rule of the copies by short form (§000049).

    A rule that a spec of the project in force names in `replaces` gets the status `replaced`.

    Args:
        specs: The specs of the project.
        upstream: The specs of the copies.

    Returns:
        The status by short form.
    """
    replaced = frozenset(
        e for s in specs if s.status in IN_FORCE for e in s.entries("replaces") or () if ":" in e
    )
    return {s.short: "replaced" if s.short in replaced else s.status for s in upstream}


def _read(path: Path) -> str | None:
    """Return the text of a file, or None when it does not exist.

    Args:
        path: The file.

    Returns:
        The text, or None.
    """
    return source(path) if path.is_file() else None


def _line(text: str, message: str) -> int:
    """Return the line that an error names (§000065).

    Args:
        text: The text of the file.
        message: The error without the path.

    Returns:
        The first line with an entry or a reference of the message, else the line of the front
        matter key at the start of the message, else 1.
    """
    lines = tuple(enumerate(text.splitlines(), 1))
    key = message.split(" ", 1)[0]
    return next(
        (
            n
            for needle in (*QUOTED.findall(message), *NAMED_REF.findall(message))
            for n, line in lines
            if needle in line
        ),
        next((n for n, line in lines if key in KEYS and line.startswith(f"{key}:")), 1),
    )


def with_line(root: Path, error: str) -> str:
    """Add the line to an error of a file, as `<path>:<line>: <message>` (§000065).

    Args:
        root: The root of the project.
        error: The error as `<path>: <message>`.

    Returns:
        The error with the line, or the same error for a folder or a missing file.
    """
    rel, _, message = error.partition(": ")
    path = root / rel
    return (
        f"{rel}:{_line(source(path, 'ignore'), message)}: {message}"
        if message and path.is_file()
        else error
    )


def run(project: Project, *, write: bool) -> tuple[int, Errors]:
    """Run every check. With `write`, write the index, its copy and `AGENTS.md` first.

    Args:
        project: The project.
        write: True to write `specs/README.md` and `AGENTS.md`.

    Returns:
        The count of specs and the errors.
    """
    specs, layout = project.load()
    copied = project.load_upstream()
    foreign = foreign_status(specs, copied)
    ctx = Context(project, {s.number: s for s in specs}, foreign)
    text = index(project, specs, foreign, copied)
    agents_path = project.root / AGENTS
    upstream = tuple(s for s in copied if foreign.get(s.short) == "approved")
    agents_on = project.config.on("agents")
    agents = merge(_read(agents_path), block(specs, upstream)) if agents_on else None
    if write:
        write_text(project.index_path, text)
    if write and agents is not None:
        write_text(agents_path, agents)
    raw = {s.short: s.status for s in copied}
    return len(specs), tuple(
        with_line(project.root, e)
        for e in (
            *layout,
            *_upstream_errors(project),
            *_lock_errors(project),
            *_check_replaces(ctx, specs, raw),
            *_number_errors(project, specs),
            *(e for s in specs for e in (*_check_meta(ctx, s), *_check_body(ctx, s))),
            *_base_errors(project, specs),
            *_schema_errors(project, specs),
            *(
                ()
                if _read(project.index_path) == text
                else ("specs/README.md: the index is not current; run spezi install (000007)",)
            ),
            *(
                ()
                if agents is None or _read(agents_path) == agents
                else (
                    f"{AGENTS}: the rules for agents are not current; run spezi install (000079)",
                )
            ),
            *_code_refs(ctx),
        )
    )
