"""Exact path matching fork."""

from typing import Any, Callable
from pyresponse.fork.fork import CallableEndpoint, Endpoint, Fork, UnmatchedEndpoint
from pyresponse.request.request import Request


class Path(Fork):
    """Route fork matching exact request URI path."""

    def __init__(self, path: str, endpoint: Endpoint | Callable[[Request], Any]) -> None:
        self._path = path
        self._endpoint = endpoint

    async def route(self, request: Request) -> Endpoint:
        path = await request.path()
        if path == self._path:
            return (
                self._endpoint
                if isinstance(self._endpoint, Endpoint)
                else CallableEndpoint(self._endpoint)
            )
        return UnmatchedEndpoint()


ForkPath = Path
