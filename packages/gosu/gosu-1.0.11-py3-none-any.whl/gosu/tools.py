import json
import subprocess
from typing import List

from plumbum import FG, ProcessExecutionError, local


def env_from_sourcing(source_path, include_unexported_variables=True):
    source = "{}source {}".format(
        "set -a && " if include_unexported_variables else "", source_path
    )
    dump = 'python3 -c "import os, json; print(json.dumps(dict(os.environ)))"'
    with subprocess.Popen(
        ["/bin/bash", "-c", f"{source} && {dump}"], stdout=subprocess.PIPE
    ) as pipe:
        return json.loads(pipe.stdout.read())


def manage_env_vars():
    try:
        from dotenv import dotenv_values

        env_vars = dotenv_values(".env")
        for name, value in env_vars.items():
            local.env[name] = value
        return env_vars
    except ModuleNotFoundError:
        print("dotenv not found, dotenv autoloading disabled")  # noqa


def get_project():
    if "DJANGO_SETTINGS_MODULE" not in local.env:
        return "example"
    else:
        return local.env["DJANGO_SETTINGS_MODULE"].split(".")[0]


def _run_venv(cmds: List[str]):
    manage_env_vars()
    print(cmds)  # noqa
    try:
        local.get(f".venv/bin/{cmds[0]}")[cmds[1:]] & FG
    except ProcessExecutionError as e:
        exit(1)
