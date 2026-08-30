"""Exact path matching fork."""

from typing import Any, Callable

from pyresponse.fork.as_endpoint import AsEndpoint
from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.fork import Fork
from pyresponse.fork.unmatched import Unmatched
from pyresponse.request.request import Request


class Path(Fork):
    """Route fork matching exact request URI path."""

    def __init__(self, path: str, endpoint: Endpoint | Callable[[Request], Any]) -> None:
        self._path = path
        self._endpoint = endpoint

    async def route(self, request: Request) -> Endpoint:
        path = await request.path()
        if path == self._path:
            return await AsEndpoint(self._endpoint).route(request)
        return Unmatched()
