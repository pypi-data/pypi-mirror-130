from json.decoder import JSONDecodeError
import re
from pathlib import Path
import json
from subprocess import run

from nygen.lib.exceptions import CondaException


RE_ENVJUNK = re.compile("[ #].*")


def clean_env_line(line: str) -> str:
    return RE_ENVJUNK.sub("", line)


def get_envs() -> list[str]:
    """Get a list of conda environments"""
    proc = run(["conda", "info", "--envs"], text=True, capture_output=True)
    lines = proc.stdout.splitlines()
    lines = [clean_env_line(line) for line in lines]
    envs = [line.casefold() for line in lines if line]
    return envs


def create_conda(name: str, python: str) -> str:
    """Create a new Conda environment"""
    args = ["conda", "create", "--json", "-y", "--name", name, f"python={python}"]
    proc = run(args, text=True, capture_output=True)
    if proc.returncode != 0:
        raise CondaException("Error creating conda environment:\n{proc.stderr}")
    try:
        j: dict = json.loads(proc.stdout)
    except JSONDecodeError:
        raise CondaException("Error creating conda environment:\n{proc.stderr}")
    conda_path = Path(j["prefix"])
    python_path = conda_path / "python.exe"
    return str(python_path)


def conda_exists(name):
    """Check whether a particular Conda environment already exists"""
    return name.casefold() in get_envs()
