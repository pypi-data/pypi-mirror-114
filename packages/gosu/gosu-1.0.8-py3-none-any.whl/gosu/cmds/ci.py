import typer
import os
import re
import semver
import subprocess


app = typer.Typer()


def git(*args):
    return subprocess.check_output(["git"] + list(args))


def get_version():
    try:
        return git("describe", "--tags").decode().strip()
    except subprocess.CalledProcessError:
        return "1.0.0"


@app.command()
def push_repo():
    git("remote", "set-url", "--push", "origin", re.sub(r'.+@([^/]+)/', r'git@\1:', os.environ["CI_REPOSITORY_URL"]))
    git("push", '-o', 'ci.skip', "origin", get_version())


@app.command()
def bump_version():
    v = get_version()
    n = semver.bump_patch(v)
    if '-' not in v:
        return

    print(f"bump from {v} to {n}")
    git("tag", n)
