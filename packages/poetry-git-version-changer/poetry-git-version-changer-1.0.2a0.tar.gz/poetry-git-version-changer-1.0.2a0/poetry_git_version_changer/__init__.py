__title__ = "poetry-git-version-changer"
__author__ = "bijij"
__license__ = "Apache-2.0"
__copyright__ = "Copyright 2021-present bijij"
__version__ = "1.0.2a"

from __future__ import annotations

import atexit
import re
import pathlib
import subprocess
import os

from functools import cached_property
from typing import Optional, TYPE_CHECKING, Any, TypedDict

import tomlkit

if TYPE_CHECKING:
    from _typeshed import StrPath


VERSION_REGEX = r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]'

DEBUG: bool = (os.getenv("POETRY_GIT_DEBUG") or "false").lower() == "true"


class _MissingSentinel:
    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "..."


MISSING: Any = _MissingSentinel()


class _Config(TypedDict):
    enabled: bool
    version_file: str
    version_regex: str


def _find_file(name: str, root: Optional[StrPath] = None) -> Optional[StrPath]:
    if root is None:
        root = pathlib.Path.cwd()
    if not isinstance(root, pathlib.Path):
        root = pathlib.Path(root)

    for level in (root, *root.parents):
        if (level / name).is_file():
            return level / name

    return None


class _Project:
    def __init__(self) -> None:
        self.patched: bool = False

    @cached_property
    def pyproject_path(self) -> StrPath:
        file = _find_file("pyproject.toml")

        if file is None:
            raise RuntimeError("Could not find pyproject.toml")

        return file

    @cached_property
    def config(self) -> _Config:
        with open(self.pyproject_path, "r", encoding="utf-8") as f:
            pyproject = tomlkit.parse(f.read())

        default: _Config = {
            "enabled": False,
            "version_file": "",
            "version_regex": VERSION_REGEX,
        }
        config: _Config = dict(pyproject["tool"]["poetry-git-version-changer"])  # type: ignore
        return default | config

    @cached_property
    def version_path(self) -> StrPath:
        return self.config["version_file"]

    @cached_property
    def original_version(self) -> str:
        return _get_version(self.version_path, self.config["version_regex"])

    @cached_property
    def version(self) -> str:
        version = self.original_version

        if version.endswith(("a", "b", "rc")):
            version = _append_commit(version)

        return version


def _append_commit(version: str) -> str:
    try:
        p = subprocess.Popen(("git", "rev-list", "--count", "HEAD"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = p.communicate()
        if out:
            version += out.decode("utf-8").strip()

        p = subprocess.Popen(("git", "rev-parse", "--short", "HEAD"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = p.communicate()
        if out:
            version += "+g" + out.decode("utf-8").strip()

    except Exception:
        pass

    return version


def _get_version(path: StrPath, regex: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        match = re.search(regex, f.read(), re.MULTILINE)

    if match is None:
        raise RuntimeError("Unable to find version string in {}".format(path))

    return match.group(1)

    if version.endswith(("a", "b", "rc")):
        version = _append_commit(version)

    return version


def _apply_version(project: _Project) -> None:
    with open(project.pyproject_path, "r", encoding="utf-8") as f:
        pyproject = tomlkit.parse(f.read())

    if pyproject["tool"]["poetry"]["version"] != project.version:  # type: ignore
        pyproject["tool"]["poetry"]["version"] = project.version  # type: ignore

        with open(project.pyproject_path, "w", encoding="utf-8") as f:
            tomlkit.dumps(pyproject)

    project.patched = True


def _revert_version(project: _Project) -> None:
    with open(project.pyproject_path, "r", encoding="utf-8") as f:
        pyproject = tomlkit.parse(f.read())

    if pyproject["tool"]["poetry"]["version"] == project.version:  # type: ignore
        pyproject["tool"]["poetry"]["version"] = project.original_version  # type: ignore

        with open(project.pyproject_path, "w", encoding="utf-8") as f:
            tomlkit.dumps(pyproject)

    project.patched = False


project: _Project = MISSING


def activate():
    global project

    if DEBUG:
        print("Activating version changer")

    project = _Project()

    if DEBUG:
        print("Loaded Project")
        print(" - Enabled: {}".format(project.config["enabled"]))
        print(" - Version File: {}".format(project.version_path))
        print(" - Original Version: {}".format(project.original_version))
        print(" - Current Version: {}".format(project.version))

    if not project.config["enabled"]:
        return

    if DEBUG:
        print("Applying new version")

    _apply_version(project)

    atexit.register(deactivate)


def deactivate():

    if DEBUG:
        print("Deactivating version changer")

    if project.patched:
        if DEBUG:
            print("Reverting version")
        _revert_version(project)
