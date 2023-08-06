import os
import re
import subprocess

import semver
import typer

app = typer.Typer()


def git(*args):
    return subprocess.check_output(["git"] + list(args))


def get_version():
    return git("describe", "--tags").decode().strip()


@app.command()
def push_repo():
    git(
        "remote",
        "set-url",
        "--push",
        "origin",
        re.sub(r".+@([^/]+)/", r"git@\1:", os.environ["CI_REPOSITORY_URL"]),
    )
    git("push", "-o", "ci.skip", "origin", get_version())


@app.command()
def bump_version():
    try:
        v = get_version()
        n = semver.bump_patch(v)
    except (subprocess.CalledProcessError, ValueError):
        print("initialise versioning with 1.0.0")
        git("tag", "1.0.0")
        return

    if "-" not in v:
        return

    print(f"bump from {v} to {n}")
    git("tag", n)
