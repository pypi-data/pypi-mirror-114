# Standard Library
from typing import Optional

# Third Party Libraries
import typer

app = typer.Typer()


@app.command()
def run(database_name: Optional[str]):
    typer.secho(f"running analyzer for database {database_name}")
