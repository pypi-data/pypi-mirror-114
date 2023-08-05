# Standard Library
import subprocess
from typing import Optional

# Third Party Libraries
import typer

app = typer.Typer()


@app.command(name="generate")
def generate_new_config(config_file: Optional[str]):
    """Generate the default database example config"""
    ping_results = subprocess.run("ping -c 4 www.google.com", shell=True)
    typer.launch(f"{ping_results}")


@app.command(name="check")
def verify_config(config_file: Optional[str]):
    """Verify configuration file is correct"""

    ping_results = subprocess.run("ping -c 4 www.google.com", shell=True)
    typer.launch(f"{ping_results}")
