try:
    # import backport of 3.10 import.metadata, if available
    from importlib_metadata import EntryPoint, EntryPoints, entry_points
except ImportError:
    from importlib.metadata import EntryPoint, EntryPoints, entry_points

from importlib.abc import Traversable
import importlib.resources
from pathlib import Path
from typing import Iterator

from nygen.lib.exceptions import TemplateException


def get_template_files(name: str) -> Iterator[tuple[Traversable, Path]]:
    try:
        eps: EntryPoints = entry_points(group="nygen.templates", name=name)
        ep: EntryPoint = next(iter(eps))
    except StopIteration:
        raise TemplateException(f"Invalid template: {name!r}")

    module = ep.load()
    root = importlib.resources.files(module)
    files = iterfiles(root)
    return files


def iterfiles(f: Traversable) -> Iterator[tuple[Traversable, Path]]:
    if not f.is_dir():
        return
    for c in f.iterdir():
        yield from _iterfiles(c)


def _iterfiles(f: Traversable, path: Path = Path()) -> Iterator[tuple[Traversable, Path]]:
    path = path / f.name
    if f.name.startswith("_") or f.name.endswith(".pyc"):
        return
    if f.is_file():
        yield f, path
    else:
        for c in f.iterdir():
            yield from _iterfiles(c, path)
