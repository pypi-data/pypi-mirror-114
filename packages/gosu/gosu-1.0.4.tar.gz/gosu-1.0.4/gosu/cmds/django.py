from typing import List
from gosu.tools import get_project, manage_env_vars, _run_venv
from gosu.cmds.python import fix
import typer
import os
from plumbum import FG, local, ProcessExecutionError


def _pm(cmds: List[str]):
    manage_env_vars()
    _run_venv(["python", "-m", f"{get_project()}.manage", *cmds])


def pm(ctx: typer.Context):
    _pm(ctx.args)


def migrate():
    _pm(["makemigrations"])
    _pm(["migrate"])


def req():
    files = ["requirements_base.txt"]
    reqs = []
    while len(files) > 0:
        file = files.pop()
        with open(file) as f:
            for line in f.readlines():
                r = line.strip()
                if r.startswith("#"):
                    continue
                if r.startswith("-r"):
                    files.append(r.split(" ")[1])
                else:
                    reqs.append(r)
    os.makedirs("dist", exist_ok=True)
    with open("requirements_compiled.txt", "w") as f:
        f.writelines([x + "\n" for x in sorted(reqs, key=str.lower)])


def test():
    fix()
    manage_env_vars()

    local.env["DEFAULT_CACHE"] = "locmemcache://"
    local.env["QUEUE_CACHE"] = "locmemcache://"
    rcfile = f"--rcfile={os.path.dirname(__file__)}/../.coveragerc"
    _run_venv(
        [
            "coverage",
            "run",
            rcfile,
            "--parallel-mode",
            "--concurrency=multiprocessing",
            f"{get_project()}/manage.py",
            "test",
            ".",
            get_project(),
            # "--parallel=3",
        ]
    )
    _run_venv(["coverage", "combine", rcfile])
    _run_venv(["coverage", "report", rcfile])
    try:
        local.cmd.flake8["--config", f"{os.path.dirname(__file__)}/../.flake8"] & FG
    except ProcessExecutionError as e:
        exit(1)


def build():
    test()
    local.cmd.python3["setup.py", "sdist", "--formats=bztar"] & FG
    req()
    local.cmd.python3["setup.py", "clean"] & FG


def notebook():
    local.env["DJANGO_ALLOW_ASYNC_UNSAFE"] = True
    _pm(["shell_plus", "--notebook"])
