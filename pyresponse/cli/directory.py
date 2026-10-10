"""Filesystem directory domain objects in Pure OOP."""

import os
from typing import Protocol

__all__ = [
    "Directory",
    "CurrentDirectory",
    "CustomDirectory",
]


class Directory(Protocol):
    """Protocol representing a filesystem directory."""

    def path(self) -> str:
        ...


class CurrentDirectory:
    """Represents the current working directory."""

    def path(self) -> str:
        return os.getcwd()


class CustomDirectory:
    """Represents an explicitly specified filesystem directory."""

    def __init__(self, dir_path: str) -> None:
        self._dir_path = dir_path

    def path(self) -> str:
        return self._dir_path
