from pathlib import Path
import typer


def create_config(config_file: Path):
    typer.confirm(
        "No config file exists yet\nShould we create one?", abort=True, default=None
    )

    config_file.touch()

    lines = [
        "# Populate the root value with a parent directory to scan for .git folders",
        "# Directories are scanned recursively",
        "ROOT=",
    ]

    with config_file.open("a") as c:
        for line in lines:
            c.write(line + "\n")
    typer.launch(str(config_file))
    print("Once the config file is populated rerun the last command")


def check_config():
    config_file = Path.home() / ".ggit.conf"

    if config_file.exists():
        lines = config_file.read_text().splitlines()
        # filter out lines starting with #
        lines = [l for l in lines if not l.startswith("#")]
        # convert to dictionary of values
        # allows for additional config variables to be added
        return {l.split("=")[0]: l.split("=")[1] for l in lines}

    if not config_file.exists():
        create_config(config_file)
        raise typer.Abort()
