from pathlib import Path
import typer


def create_config(config_file: Path):
    print("No config file exists yet")
    ans = typer.prompt("Should we create one? (Y/n)")

    while ans.lower() not in ["y", "n"]:
        ans = typer.prompt("Please reply with y or n")

    if ans.lower() == "n":
        typer.Abort()

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
    print("Once the config file is poplulated rerun the last command")


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
