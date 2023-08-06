from pathlib import Path
import json
import os
from importlib.abc import Traversable

from nygen.conf import load_conf
from nygen.lib.formatter import Formatter
from nygen.lib.conda import create_conda, conda_exists
from nygen.lib.exceptions import BadProjectNameException, DestinationExistsException, CondaEnvironmentExistsException, TemplateException
from nygen.lib.template import get_template_files


def is_dir_empty(p: Path) -> bool:
    try:
        next(p.iterdir())
        is_empty = False
    except StopIteration:
        is_empty = True
    return is_empty


def precheck_name(path_maps, name) -> None:
    # Duplicate path_map destinations means bad project name, such as "docs" or "tests"
    if len(set(dst for src, dst in path_maps)) != len(path_maps):
        raise BadProjectNameException(f"Project name is invalid: {name}")


def precheck_dst(dstpath: Path) -> None:
    if dstpath.exists() and not is_dir_empty(dstpath):
        raise DestinationExistsException(f"Destination path not empty: {dstpath.absolute()}")


def precheck_conda(name):
    if conda_exists(name):
        raise CondaEnvironmentExistsException(f"Conda environment already exists: {name}")


def get_path_maps(dst_root: Path, formatter: Formatter, template: str) -> list[tuple[Path, Path]]:
    path_maps: list[tuple[Path, Path]] = []
    for src, rel_src in get_template_files(template):
        dst = dst_root / Path(formatter.format(str(rel_src)))
        path_maps.append((src, dst))
    return path_maps


def gen_project(name, cmd_vars: dict[str, str], open_proj: bool, open_dir: bool, template: str):
    print(f"Generating project {name}")
    conf, conf_vars = load_conf()
    formatter = Formatter(cmd_vars=cmd_vars, conf_vars=conf_vars)
    formatter["name"] = name

    dst_root = Path(name)

    formatter.fill_defaults()

    formatter.precheck()
    path_maps = get_path_maps(dst_root, formatter, template)

    precheck_name(path_maps, name)
    precheck_dst(dst_root)
    precheck_conda(name)

    print(f"Creating conda environment {name!r} with Python {formatter['python']}")
    python_path = create_conda(name, formatter["python"])
    formatter["python_path"] = json.dumps(python_path).removeprefix('"').removesuffix('"')

    print("Generating file structure")
    for src, dst in path_maps:
        gen_file(src, dst, formatter)

    print(f"Successfully created project at {dst_root.absolute()}")
    if open_proj:
        os.startfile(dst_root.absolute() / f"{name}.code-workspace")
    if open_dir:
        os.startfile(dst_root.absolute())


def gen_file(src: Path, dst: Path, formatter: Formatter):
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(formatter.format(src.read_text()))
