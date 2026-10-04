"""Development tasks. Run with `uv run invoke <task>`; CI runs the same tasks."""

from invoke.context import Context
from invoke.tasks import task


@task
def format(c: Context) -> None:
    """Fix lint issues and format the code."""
    c.run("ruff check --fix", echo=True)
    c.run("ruff format", echo=True)


@task
def lint(c: Context) -> None:
    """Lint, format-check and type-check the template's own tooling."""
    c.run("ruff check", echo=True)
    c.run("ruff format --check", echo=True)
    c.run("mypy", echo=True)


@task
def test(c: Context) -> None:
    """Render every variant and run its lint and test tasks."""
    c.run("pytest", echo=True)


@task
def render(c: Context, dest: str, api: bool = False) -> None:
    """Render the working tree into DEST with default answers."""
    c.run(
        "copier copy --trust --vcs-ref HEAD --defaults"
        " -d project_name=Demo -d author_name=Demo -d author_email=demo@example.com"
        f" -d api={str(api).lower()} . {dest}",
        echo=True,
    )
