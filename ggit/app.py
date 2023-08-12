from pathlib import Path
import subprocess
import typer
from helpers import check_config, pull_git_element, create_table
from rich.progress import track


app = typer.Typer(
    help="Check all git repos",
    epilog="Made for run with :snake:",
    rich_markup_mode="markdown",
    no_args_is_help=True,
)


@app.command("get")
# Make remove_clean into an argument
def get(
    filter_clean: bool = typer.Option(False, "--filter_clean", "-fc", is_flag=True)
):
    config = check_config()

    fp = Path(config["ROOT"]).expanduser()

    branch = []
    commit_status = []
    modified = []
    project = []

    for filename in track(fp.glob("**/.git"), description="Looking..."):
        parent_folder = Path(filename).parent
        res = subprocess.run(
            ["git", "-C", parent_folder, "status"], capture_output=True, text=True
        )
        project.append(parent_folder.stem)

        # process results into nicer format
        lines = res.stdout.splitlines()

        # Filter out empty lines
        lines = [l for l in lines if not l.startswith(" ") if l != ""]

        if filter_clean:
            if any("nothing to commit" in l for l in lines):
                continue

        # Filter out specific elements from lines
        branch.append(pull_git_element(lines, "On branch", "On branch"))
        commit_status.append(pull_git_element(lines, "commit", "(.*"))
        modified.append(pull_git_element(lines, "\t", "\tmodified: "))

    # create table
    data = list(zip(project, branch, commit_status, modified))

    create_table(data)


# This one is hard to test since fetch isn't returning anything for me repos and consumes its output...
@app.command("fetch")
def fetch(prune: bool = typer.Option(False, "--prune", "p", is_flag=True)):
    config = check_config()
    fp = Path(config["ROOT"]).expanduser()

    project = []

    for filename in track(fp.glob("**/.git"), description="Fetching..."):
        project.append(parent_folder.stem)
        parent_folder = Path(filename).parent
        if prune:
            res = subprocess.run(
                ["git", "-C", parent_folder, "fetch", "-p"],
                capture_output=True,
                text=True,
            )
        else:
            res = subprocess.run(
                ["git", "-C", parent_folder, "fetch"],
                capture_output=True,
                text=True,
            )
    lines = res.stdout.splitlines()

    # Filter out empty lines
    lines = [l for l in lines if not l.startswith(" ") if l != ""]
    print(lines)


# Have an option to fetch and prune
typer.run(fetch)
