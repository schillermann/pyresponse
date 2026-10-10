"""Target candidates in Pure OOP."""

import os
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from pyresponse.cli.target import Target

from pyresponse.cli.coordinate import ExplicitCoordinate
from pyresponse.cli.directory import CurrentDirectory, Directory

__all__ = [
    "Candidate",
    "FileCandidate",
]


class Candidate(Protocol):
    """Protocol representing a candidate application target."""

    def exists(self) -> bool:
        ...

    def target(self) -> "Target":
        ...


from pyresponse.cli.explicit_target import ExplicitTarget


class FileCandidate:
    """A target candidate represented by a source file on disk."""

    def __init__(
        self,
        filename: str,
        attr: str = "app",
        directory: Directory = CurrentDirectory(),
    ) -> None:
        self._filename = filename
        self._attr = attr
        self._directory = directory

    def exists(self) -> bool:
        return os.path.isfile(os.path.join(self._directory.path(), self._filename))

    def target(self) -> ExplicitTarget:
        mod = self._filename.removesuffix(".py")
        return ExplicitTarget(ExplicitCoordinate(mod, self._attr))
