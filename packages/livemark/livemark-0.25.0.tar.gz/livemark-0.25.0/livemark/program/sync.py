import typer
import difflib
from ..project import Project
from ..document import Document
from .main import program
from . import common


@program.command(name="sync")
def program_sync(
    source: str = common.source,
    print: bool = common.print,
    diff: bool = common.diff,
):
    """Sync the article"""

    # Create document
    document = Document(source, target=source, project=Project())

    # Process document
    document.process()

    # Diff document
    if diff:
        l1 = document.input.splitlines(keepends=True)
        l2 = document.output.splitlines(keepends=True)
        ld = list(difflib.unified_diff(l1, l2, fromfile="source", tofile="target"))
        typer.secho("".join(ld), nl=False)
        raise typer.Exit()

    # Print document
    if print:
        document.print()
        raise typer.Exit()

    # Write document
    document.write()
