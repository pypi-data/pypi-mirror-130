from pathlib import Path
import importlib.resources
from importlib.metadata import entry_points
import json
import os

from nygen.conf import load_conf
from nygen.lib.formatter import Formatter
from nygen.lib.conda import create_conda, conda_exists
from nygen.lib.exceptions import BadProjectNameException, DestinationExistsException, CondaEnvironmentExistsException, TemplateException


def get_src_files(p: Path):
    if p.is_file():
        if not (p.name == "__pycache__" or p.name.endswith(".pyc")):
            yield p
    else:
        for c in p.iterdir():
            yield from get_src_files(c)


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
    try:
        template_entrypoint = next(iter(entry_points(group="nygen.templates", name=template)))
    except StopIteration:
        raise TemplateException(f"Invalid template: {template!r}")
    template_module = template_entrypoint.load()
    src_root: Path = importlib.resources.path(template_module, '.')
    srcs = get_src_files(src_root)
    path_maps = [(src, map_path(src, src_root, dst_root, formatter)) for src in srcs]
    return path_maps


def map_path(src: Path, src_root: Path, dst_root: Path, formatter: Formatter):
    rel_src = src.relative_to(src_root)
    rel_src = Path(formatter.format(str(rel_src)))
    dst = dst_root / rel_src
    return dst


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
