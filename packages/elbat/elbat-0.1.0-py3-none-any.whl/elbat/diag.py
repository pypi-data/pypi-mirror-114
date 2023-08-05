from typing import Optional
import typer


app = typer.Typer()


@app.command()
def run(diag_type: Optional[str]):
    typer.secho(f"running full table disco for {diag_type}")
