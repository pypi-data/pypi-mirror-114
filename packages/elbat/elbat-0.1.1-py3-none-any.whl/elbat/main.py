# Standard Library
from os.path import expanduser
from pathlib import Path

# Third Party Libraries
import typer

# Gluent
from elbat.commands import analyze, config, disco, offload, present


def main():
    app = typer.Typer()

    app.add_typer(offload.app, name="offload")
    app.add_typer(disco.app, name="disco")
    app.add_typer(present.app, name="present")
    app.add_typer(analyze.app, name="analyze")
    app.add_typer(config.app, name="config")

    home_path = expanduser("~")
    config_base: Path = Path(home_path) / ".elbat"
    config_base.mkdir(parents=True, exist_ok=True)
    config_path: Path = config_base / "config.yml"

    if not config_path.is_file():
        config_path.write_text("")
    typer.secho(f"Environment: loaded configuration from `{config_base}`")

    app()


if __name__ == "__main__":
    typer.run(main)
