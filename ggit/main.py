from pathlib import Path
import glob
import subprocess
import typer
from .helpers import check_config

app = typer.Typer(
    help="Check all git repos",
    epilog="Made for run with :snake:",
    rich_markup_mode="markdown",
    no_args_is_help=True,
)


@app.command()
def get():
    config = check_config()
    for filename in glob.iglob(config["ROOT"] + "**/.git", recursive=True):
        parent_folder = Path(filename).parent
        res = subprocess.run(
            ["git", "-C", parent_folder, "status"], stdout=subprocess.PIPE
        )
        # process results into nicer format
        print(res.stdout.splitlines())


@app.command()
def echo():
    print("test")


# TODO process results and display in table
# Have option to discard clean statuses
# get()
