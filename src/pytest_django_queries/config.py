import dataclasses
from functools import lru_cache
from pathlib import Path
import tomllib
from typing import Self, cast

import click

# Human readable section name in pyproject.toml
CONFIG_SECTION = "[tool.pytest-django-queries]"


class InvalidConfiguration(click.ClickException):
    """
    An exception that occurs when the tool's configuration in pyproject.toml is invalid.
    """


@dataclasses.dataclass
class Config:
    # The root directory - i.e., the directory where the pyproject.toml is.
    _root: Path

    # Filename or path (relative from the project's root) to store the results.
    report_filename: str = ".pytest-queries"
    previous_report_filename: str = ".pytest-queries.old"

    @property
    def report_path(self) -> Path:
        # TODO: before merge, this needs to prevent path traversal attacks.
        #       If the project's root is found, then we must not allow to traverse.
        #       Otherwise we may allow arbitrary file writes which can have security
        #       implications on untrusted projects.
        return Path(self._root) / self.report_filename

    @property
    def previous_report_path(self) -> Path:
        return Path(self._root) / self.previous_report_filename

    @classmethod
    def parse(cls, path: Path) -> Self | None:
        """
        :return: Returns None if no config found.
        """
        with path.open("rb") as fp:
            toml = tomllib.load(fp)

        if (cfg := toml.get("tool", {}).get("pytest-django-queries")) is None:
            return None

        if isinstance(cfg, dict) is False:
            raise InvalidConfiguration(
                f"{path}: expected a dictionary for the {CONFIG_SECTION} section "
                f"but found {cfg!r} instead."
            )
        cfg = cast(dict, cfg)
        return cls(_root=path.resolve().parent, **cfg)


@lru_cache
def _get_config(src: Path) -> Config | None:
    """
    Finds the first pyproject.toml in CWD or user-provided path that defines
    a ``[tool.pytest-django-queries]`` section.

    Either traverses until the root directory is reached, or until we reach the
    root of the git repository (if it's a git project).

    :param src: Directories the user indirectly provided via CLI inputs, e.g.,
        "django-queries /path/to/my-report.json" -> find_project_root(["/path/to/"])
    """

    # Traverse until the root directory is reached
    for directory in src.parents:
        if (pyproject := (directory / "pyproject.toml")).exists():
            config = Config.parse(pyproject)

            # Note: config must be returned even if it's blank.
            #       A blank config means the config exists whereas `None` means
            #       it doesn't.
            if config is not None:
                return config

        # If the directory contains a git-repo, then stop traversing parents
        # as it means we are leaving the project.
        if (directory / ".git").exists():
            # TODO: throw an error if we don't find a root directory.
            #       Config doesn't matter, but user should at minimum put an empty
            #       section. This will avoid headaches in the future with supporting
            #       both known and unknown project roots.
            return None
    # TODO: throw an error if we don't find a root directory
    return None


def get_config(src: Path | None = None) -> Config:
    src = src or Path.cwd()
    return _get_config(src=src) or Config(_root=src)
