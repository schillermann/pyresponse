"""In-path target decorator ensuring directories exist in sys.path in Pure OOP."""

import os
import sys
from typing import Any, Sequence

from pyresponse.fork.route_entry import RouteEntry


class InPathTarget:
    """Decorator ensuring search directories are in sys.path before loading target."""

    def __init__(self, directories: Sequence[str], origin: Any) -> None:
        self._directories = directories
        self._origin = origin

    def name(self) -> str:
        return self._origin.name()

    def load(self) -> Any:
        for directory in self._directories:
            if os.path.isdir(directory) and directory not in sys.path:
                sys.path.insert(0, directory)
        return self._origin.load()

    def routes(self) -> Sequence[RouteEntry]:
        for directory in self._directories:
            if os.path.isdir(directory) and directory not in sys.path:
                sys.path.insert(0, directory)
        return self._origin.routes()
