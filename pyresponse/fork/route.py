"""Route fork combining Path and Method in Pure OOP."""

from typing import Any

from pyresponse.fork.empty_fork import EmptyFork
from pyresponse.fork.fork_envelope import ForkEnvelope
from pyresponse.fork.method import Method
from pyresponse.fork.path import Path


class Route(ForkEnvelope):
    """Route fork matching HTTP method and request URI path."""

    def __init__(self, method: str, path: str, origin: Any = EmptyFork()) -> None:
        super().__init__(Path(path, Method(method, origin)))
