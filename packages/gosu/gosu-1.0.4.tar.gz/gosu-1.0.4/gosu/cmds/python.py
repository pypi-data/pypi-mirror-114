from gosu.tools import env_from_sourcing, manage_env_vars, _run_venv
from plumbum import FG, local
import os
import glob
from typing import List


def sh():
    manage_env_vars()
    for k, v in env_from_sourcing(".venv/bin/activate").items():
        local.env[k] = v
    local.get(local.env["SHELL"].split("/")[-1]) & FG


def venv():
    manage_env_vars()
    local.cmd.python3["-m", "venv", ".venv"] & FG
    _run_venv(["pip", "install", "-U", "pip", "wheel"])

    if os.path.isfile("requirements-gosu.txt"):
        _run_venv(["pip", "install", "-r", "requirements-gosu.txt"])

    # find all requirements
    add_reqs = glob.glob("requirement*.txt")
    for r in add_reqs:
        _run_venv(["pip", "install", "-r", r])


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


# def venv():
#     manage_env_vars()
#     local.cmd.python3["-m", "venv", ".venv"] & FG
#     run(["pip", "install", "-U", "pip", "wheel"])
#
#     if os.path.isfile("requirements-gosu.txt"):
#         run(["pip", "install", "-r", "requirements-gosu.txt"])
#
#     # install editable gosu if is existent -> dev environment
#     # if os.path.isdir("../gosu"):
#     #     run(["pip", "install", "../gosu"])
#     # else:
#     #     run(["pip", "install", glob.glob("gosu*.tar.bz2")])
#     #
#     # add_pkgs = glob.glob("*.tar.bz2")
#     # if add_pkgs:
#     #     run(["pip", "install", add_pkgs])
#
#     # find all requirements
#     add_reqs = glob.glob("requirement*.txt")
#     for r in add_reqs:
#         run(["pip", "install", "-r", r])
