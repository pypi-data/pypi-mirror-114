# Third Party Libraries
import typer

app = typer.Typer()


@app.command()
def table_status(table_owner: str, table_name: str):
    typer.secho(f"Offloading full table {table_owner}.{table_name}")


@app.command()
def full(table_owner: str, table_name: str):
    typer.secho(f"Offloading full table {table_owner}.{table_name}")


@app.command()
def merge(table_owner: str, table_name: str, source: str):
    typer.secho(f"merging {source} into {table_owner}.{table_name}")
