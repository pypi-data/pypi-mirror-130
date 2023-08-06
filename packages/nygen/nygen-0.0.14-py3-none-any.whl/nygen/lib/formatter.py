from __future__ import annotations

import collections.abc
from dataclasses import dataclass
from datetime import date
from typing import Callable, Union

import nypi

from nygen.lib.exceptions import MissingArgumentException


@dataclass
class VarDef():
    name: str
    desc: str
    cmd: bool
    conf: bool
    precheck: bool
    default: Union[str, Callable[[], str]]


class Formatter(collections.abc.Mapping):
    __slots__ = ["_vals"]
    _vars = {
        v.name: v for v in
        [
            #      NAME                 DESC                    CMD     CONF    PRECHECK    DEFAULT
            VarDef("name",              "Package name",         False,  False,  True,       None),                                          # noqa: E241
            VarDef("author",            "Author full name",     True,   True,   True,       None),                                          # noqa: E241
            VarDef("email",             "Author email",         True,   True,   True,       None),                                          # noqa: E241
            VarDef("github",            "Github username",      True,   True,   True,       None),                                          # noqa: E241
            VarDef("python",            "Python version",       True,   True,   True,       "3.9"),                                         # noqa: E241
            VarDef("_",                 "Empty string",         False,  False,  False,      ""),                                            # noqa: E241
            VarDef("year",              "Year",                 False,  False,  True,       lambda: str(date.today().year)),                # noqa: E241, E272
            VarDef("pytest_version",    "pytest version",       True,   True,   True,       lambda: nypi.get_pkg("pytest").version),        # noqa: E241, E272
            VarDef("flake8_version",    "flake version",        True,   True,   True,       lambda: nypi.get_pkg("flake8").version),        # noqa: E241, E272
            VarDef("autopep8_version",  "autopep8 version",     True,   True,   True,       lambda: nypi.get_pkg("autopep8").version),      # noqa: E241, E272
            VarDef("python_path",       "Path to python.exe",   False,  False,  False,      None),                                          # noqa: E241
        ]
    }
    cmd_vars = {name: _var for name, _var in _vars.items() if _var.cmd}
    conf_vars = {name: _var for name, _var in _vars.items() if _var.conf}

    def __init__(self, cmd_vars: dict[str, str] = None, conf_vars: dict[str, str] = None):
        self._vals: dict[str, str] = {v: None for v in self._vars}
        self.load(cmd_vars=cmd_vars, conf_vars=conf_vars)

    def __getitem__(self, key: str) -> str:
        return self._vals[key]

    def __setitem__(self, key: str, value: str) -> None:
        # raise AttributeError for invalid keys
        _ = self._vals[key]
        self._vals[key] = value

    def __len__(self):
        return len(self._vars)

    def __iter__(self):
        return iter(self._vars)

    def precheck(self) -> None:
        for name, _var in self._vars.items():
            if _var.precheck and not self[name]:
                raise MissingArgumentException(f"Missing argument: {name}")

    def fill_defaults(self) -> None:
        for name, _var in self._vars.items():
            if not self[name]:
                if callable(_var.default):
                    self[name] = _var.default()
                else:
                    self[name] = _var.default

    def to_conf(self) -> dict[str, str]:
        return {name: self[name] or "" for name in self.conf_vars}

    def load(self, *, cmd_vars: dict[str, str] = None, conf_vars: dict[str, str] = None):
        if not cmd_vars and not conf_vars:
            return

        if cmd_vars is None:
            cmd_vars = {}
        if conf_vars is None:
            conf_vars = {}

        for name, _var in self._vars.items():
            if _var.cmd and cmd_vars.get(name):
                self[name] = cmd_vars[name]
            elif _var.conf and conf_vars.get(name):
                self[name] = conf_vars[name]

    def format(self, s: str):
        return s.format(**self)
