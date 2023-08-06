import typer
from plumbum import FG, local

from gosu.cmds.python import fix

app = typer.Typer()


@app.command()
def run():
    fix()
    (
        local["coverage"][
            "run",
            "-m",
            "pytest",
            "-o",
            "console_output_style=progress",
            "--forked",
            "--numprocesses=auto",
        ]
        & FG
    )
    local["coverage"]["report", "-m"] & FG
