"""Generate COLA project scaffolds using the shipped language templates."""

import re
import uuid
from pathlib import Path

import click
from jinja2 import Environment, StrictUndefined

from .common import cli

TEMPLATES = Path(__file__).with_name("templates")
LANGUAGES = click.Choice(["cpp", "python", "fortran", "java", "julia"], case_sensitive=False)
JULIA_RESERVED_NAMES = set(
    "baremodule begin break catch const continue do else elseif end export false finally for function "
    "global if import let local macro module quote return struct true try using while "
    "abstract mutable primitive type where in isa public outer as COLA Core Base".split()
)


def project_name(ctx, param, value):
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,31}", value):
        raise click.BadParameter("use 1–32 ASCII letters, digits or underscores, starting with a letter")
    return value


def project_version(ctx, param, value):
    if not re.fullmatch(r"\d+\.\d+\.\d+", value):
        raise click.BadParameter("use a numeric major.minor.patch version, e.g. 1.0.0")
    return value


def render_project(name, language, version):
    environment = Environment(undefined=StrictUndefined, keep_trailing_newline=True, autoescape=False)
    context = {
        "name": name,
        "package": name.lower() + "_filters",
        "version": version,
        "language": language,
        "uuid": str(uuid.uuid4()),
    }
    groups = ["common"]
    if language in ("cpp", "fortran", "java"):
        groups.append("quality")
    groups.append(language)
    files = {}
    for group in groups:
        directory = TEMPLATES / group
        for template in sorted(directory.rglob("*.j2")):
            path = environment.from_string(template.relative_to(directory).as_posix()[:-3]).render(context)
            files[path] = environment.from_string(template.read_text(encoding="utf-8")).render(context)
    return files


def write_project(name, prefix, version, language, force, section=None):
    if language == "julia" and name in JULIA_RESERVED_NAMES:
        raise click.ClickException(f"Reserved Julia module name: {name}")
    files = render_project(name, language, version)
    if section == "cmake":
        if language in ("python", "julia"):
            build_file = "pyproject.toml" if language == "python" else "Project.toml"
            raise click.ClickException(
                f"{language} projects use {build_file}; use 'setup project --language {language}'."
            )
        files = {p: text for p, text in files.items() if "cmake" in p.lower() or p == "CMakeLists.txt"}
    elif section == "sources":
        files = {p: text for p, text in files.items() if p.startswith(("src/", "include/"))}
    elif section == "git":
        files = {".gitignore": files[".gitignore"]}
    root = Path(prefix).expanduser() / name
    if root.is_symlink() or (root.exists() and not root.is_dir()):
        raise click.ClickException(f"Project path is not a regular directory: {root}")
    if section is None and root.exists() and any(root.iterdir()) and not force:
        raise click.ClickException(f"Directory is not empty: {root}. Use --force to overwrite generated files.")
    # Check all destinations before writing, including symlinks inside an existing project.
    for relative in files:
        target = root / relative
        for component in (target, *target.parents):
            if component == root.parent:
                break
            if component.is_symlink():
                raise click.ClickException(f"Refusing to write through a symlink: {component}")
            if component != target and component.exists() and not component.is_dir():
                raise click.ClickException(f"Not a directory: {component}")
        if target.exists() and (target.is_dir() or not force):
            raise click.ClickException(f"File already exists: {target}. Use --force to overwrite generated files.")
    try:
        if language == "julia" and "Project.toml" in files and (root / "Project.toml").is_file():
            header = (root / "Project.toml").read_text(encoding="utf-8").split("[", 1)[0]
            match = re.search(r'^uuid\s*=\s*"([^"]+)"', header, re.MULTILINE)
            if match:
                try:
                    project_uuid = str(uuid.UUID(match[1]))
                except ValueError as error:
                    raise click.ClickException("Invalid UUID in existing Project.toml") from error
                files["Project.toml"] = re.sub(
                    r'^uuid = ".*"', f'uuid = "{project_uuid}"', files["Project.toml"], flags=re.MULTILINE
                )
        for relative, content in files.items():
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
    except OSError as error:
        raise click.ClickException(str(error)) from error
    click.echo(f"Created {language} project files in {root}")


def options(function):
    for decorator in (
        click.option("--force", is_flag=True, help="Overwrite generated files; keep unrelated files."),
        click.option("--version", default="1.0.0", callback=project_version, show_default=True),
        click.option(
            "--prefix",
            default="./",
            type=click.Path(file_okay=False),
            show_default=True,
            help="Parent directory for the new project.",
        ),
        click.option("--language", "-l", type=LANGUAGES, default="cpp", show_default=True),
        click.option("--name", required=True, callback=project_name, help="Project/module name."),
    ):
        function = decorator(function)
    return function


@cli.group()
def setup():
    """Create COLA projects and individual project components."""


@setup.command()
@options
def project(**kwargs):
    """Create a C++, Python, Fortran, Java or Julia project scaffold."""
    write_project(**kwargs)


@setup.command()
@options
def cmake(**kwargs):
    """Generate just the native build files (legacy command)."""
    write_project(**kwargs, section="cmake")


@setup.command()
@options
def sources(**kwargs):
    """Generate just the imports and filter declarations."""
    write_project(**kwargs, section="sources")


@setup.command()
@options
def git(**kwargs):
    """Generate .gitignore without initializing a repository."""
    write_project(**kwargs, section="git")


@cli.command()
def version():
    from colapy import __version__

    click.echo(f"COLA CLI {__version__}")
