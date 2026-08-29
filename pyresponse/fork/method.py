"""HTTP Method matching fork."""

from typing import Any, Callable
from pyresponse.fork.fork import CallableEndpoint, Endpoint, Fork, UnmatchedEndpoint
from pyresponse.request.request import Request


class Method(Fork):
    """Route fork matching HTTP request method."""

    def __init__(self, method: str, endpoint: Endpoint | Callable[[Request], Any]) -> None:
        self._method = method
        self._endpoint = endpoint

    async def route(self, request: Request) -> Endpoint:
        method = await request.method()
        if method.upper() == self._method.upper():
            return (
                self._endpoint
                if isinstance(self._endpoint, Endpoint)
                else CallableEndpoint(self._endpoint)
            )
        return UnmatchedEndpoint()


ForkMethod = Method
