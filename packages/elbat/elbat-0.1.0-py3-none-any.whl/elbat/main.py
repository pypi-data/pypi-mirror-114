import typer
from loguru import logger
from elbat import offload, disco, present, analyze

app = typer.Typer()
app.add_typer(offload.app, name="offload")
app.add_typer(disco.app, name="disco")
app.add_typer(present.app, name="present")
app.add_typer(present.app, name="analyze")


if __name__ == "__main__":
    app()
