import glob
import os
from typing import List

import typer
from plumbum import FG, local

from gosu.tools import _run_venv, env_from_sourcing, manage_env_vars

app = typer.Typer()


@app.command()
def sh():
    manage_env_vars()
    for k, v in env_from_sourcing(".venv/bin/activate").items():
        local.env[k] = v
    local.get(local.env["SHELL"].split("/")[-1]) & FG


@app.command()
def venv(env: str = typer.Argument("dev")):
    manage_env_vars()
    local.cmd.python3["-m", "venv", ".venv"] & FG
    _run_venv(["pip", "install", "-U", "pip", "wheel"])
    if env == "dev":
        _run_venv(["pip", "install", "-e", "."])

    r = f"requirements/{env}.txt"
    if os.path.isfile(r):
        _run_venv(["pip", "install", "-r", f"requirements/{env}.txt"])


@app.command()
def run(cmds: List[str]):
    _run_venv(cmds)


def _get_pkg_pyfiles():
    files = list(
        filter(
            lambda e: all(
                [not (x in e) for x in ["node_modules", "migrations", "build"]]
            ),
            glob.glob("**/*.py", recursive=True),
        )
    )
    print(files)  # noqa
    return files


@app.command()
def fix(env: str = typer.Argument("dev")):
    if env == "dev":
        (
            local.cmd.pyupgrade.__getitem__(
                ["--py38-plus", "--exit-zero-even-if-changed", *_get_pkg_pyfiles()]
            )
            & FG
        )
        local.cmd.isort.__getitem__(["--profile", "black", *_get_pkg_pyfiles()]) & FG
        local.cmd.black.__getitem__([*_get_pkg_pyfiles()]) & FG
    else:
        local.cmd.pyupgrade.__getitem__(["--py38-plus", *_get_pkg_pyfiles()]) & FG
        (
            local.cmd.isort.__getitem__(
                ["--profile", "black", "-c", *_get_pkg_pyfiles()]
            )
            & FG
        )
        local.cmd.black.__getitem__(["--check", *_get_pkg_pyfiles()]) & FG


@app.command()
def test(env: str = typer.Argument("dev")):
    fix(env)
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
