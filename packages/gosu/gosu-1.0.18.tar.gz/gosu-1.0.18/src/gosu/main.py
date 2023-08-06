import glob
import os
import re
import subprocess
import sys
import traceback
from multiprocessing import Pool
from pathlib import Path

import typer
from plumbum import local

from gosu import cmds

app = typer.Typer()
app.add_typer(cmds.ci.app, name="ci")
app.add_typer(cmds.python.app, name="python")
app.add_typer(cmds.django.app, name="django")


def get_project_root():
    stack = reversed(traceback.extract_stack())

    for frame in stack:
        try:
            path = Path(frame.filename).resolve()
        except OSError:
            # some frames have names that cannot be treated as file paths
            continue

        # packages installed using pip are stored in the 'site-packages'
        # if from_root is called from a package, we can quickly find the root directory
        posix_like = path.as_posix()
        if "site-packages" in posix_like:
            root_path = Path(re.compile(r".*site-packages/.*?/").findall(posix_like)[0])
            # but we ignore 'from_root' package
            if root_path.name != "from_root":
                return root_path

        while path.parents:
            if (
                (path / ".git").exists()
                or (path / ".project-root").exists()
                or (path / "setup.py").exists()
            ):
                return path

            path = path.parent

    raise FileNotFoundError(
        'There is neither ".git" directory nor ".project-root" file nor "setup.py", cannot detect root folder'
    )


def safe_run(cmd, **kwargs):
    r = subprocess.run(cmd, capture_output=True, **kwargs)
    if r.returncode != 0:
        sys.stdout.write(r.stdout.decode("utf8"))
        sys.stdout.write(r.stderr.decode("utf8"))
        raise Exception("error with", cmd)


def pbuild(file):
    project_base = os.path.abspath(local.cwd + "/" + file.split("/")[0])
    project_name = project_base.split("/")[-1]
    print(f"build {project_base}")  # noqa
    safe_run(["gosu", "venv"], cwd=project_base)
    safe_run(["gosu", "build"], cwd=project_base)
    safe_run(
        ["cp", glob.glob(project_base + "/dist/*.tar.bz2")[0], "../dist"],
        cwd=project_base,
    )
    safe_run(
        [
            "cp",
            glob.glob(project_base + "/dist/requirements_compiled.txt")[0],
            f"../dist/requirements_{project_name}.txt",
        ],
        cwd=project_base,
    )


def build_all():
    safe_run(["mkdir", "-p", "dist"])
    with Pool(3) as p:
        p.map(pbuild, glob.glob("**/setup.py"))


def import_from_path(path, module_name):
    import importlib.util

    spec = importlib.util.spec_from_file_location(module_name, path)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo


def find_local_gosu_cmds():
    cmds_path = os.getcwd() + "/cmds.py"
    if not os.path.isfile(cmds_path):
        return

    import_from_path(cmds_path, "gosu.user.cmds")


find_local_gosu_cmds()
