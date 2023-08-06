from gosu.tools import env_from_sourcing, manage_env_vars, _run_venv
from plumbum import FG, local
import glob
from typing import List
import typer
import os

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


def fix():
    local.cmd.pyupgrade.__getitem__(["--py38-plus", *_get_pkg_pyfiles()]) & FG
    local.cmd.isort.__getitem__(["--profile", "black", *_get_pkg_pyfiles()]) & FG
    local.cmd.black.__getitem__([*_get_pkg_pyfiles()]) & FG
