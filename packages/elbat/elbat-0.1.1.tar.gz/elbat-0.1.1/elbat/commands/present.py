# Third Party Libraries
import typer

app = typer.Typer()


@app.command(name="table")
def present_table(table_owner: str, table_name: str):
    typer.secho(f"running full table disco for {table_owner}.{table_name}")
