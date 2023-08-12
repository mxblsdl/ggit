from pathlib import Path
import typer
from rich.prompt import Confirm
from rich.console import Console
from rich.table import Table


def create_config(config_file: Path):
    res = Confirm.ask("No config file exists yet\nShould we create one?")
    if not res:
        raise typer.Abort()

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


def pull_git_element(lines: list, el_str: str, rep_str: str, els: int = 0) -> str:
    el = [l for l in lines if el_str in l]
    if not el:
        return ''

    return el[els].replace(rep_str, "")


def create_table(data: list[list]) -> None:
        table = Table(title="Global Git Status", show_lines=True)

        table.add_column("Project", justify="center", style="blue")
        table.add_column("Current Branch", style="magenta")
        table.add_column("Commits", justify="center", style="green")
        table.add_column("Modified", justify="left", style="on dodger_blue2")


        for d in data:
            table.add_row(
                d[0],
                d[1],
                d[2],
                d[3],
            )

        console = Console()
        console.print(table)