"""Regex path matching fork."""

import re
from typing import Any, Callable
from pyresponse.fork.fork import CallableEndpoint, Endpoint, Fork, UnmatchedEndpoint
from pyresponse.request.params import WithParams
from pyresponse.request.request import Request
from pyresponse.response.response import Response


class EndpointWithParams(Endpoint):
    """Endpoint decorator injecting parsed route parameters into the Request."""

    def __init__(self, origin: Endpoint, params: dict[str, str]) -> None:
        self._origin = origin
        self._params = params

    def is_matched(self) -> bool:
        return True

    async def response(self, request: Request) -> Response:
        return await self._origin.response(WithParams(request, self._params))


class Regex(Fork):
    """Route fork matching URI path via regular expression pattern."""

    def __init__(self, pattern: str, endpoint: Endpoint | Callable[[Request], Any]) -> None:
        self._pattern = pattern
        self._endpoint = endpoint

    async def route(self, request: Request) -> Endpoint:
        path = await request.path()
        match = re.match(self._pattern, path)
        if match:
            endpoint_obj = (
                self._endpoint
                if isinstance(self._endpoint, Endpoint)
                else CallableEndpoint(self._endpoint)
            )
            params = match.groupdict()
            if params:
                return EndpointWithParams(endpoint_obj, params)
            return endpoint_obj
        return UnmatchedEndpoint()


ForkRegex = Regex
ResourceWithParams = EndpointWithParams
