"""Regex URI path matching fork in Pure OOP."""

import re
from collections.abc import Callable as TypingCallable
from typing import Any

from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.source_endpoint import SourceEndpoint
from pyresponse.fork.fork import Fork
from pyresponse.fork.route_entry import EndpointRoutes, RouteEntry
from pyresponse.fork.missing_endpoint import MissingEndpoint
from pyresponse.fork.with_params import WithParams
from pyresponse.request.request import Request



class Regex(Fork):
    """Route fork matching request path using regular expressions and extracting named parameters."""

    def __init__(
        self,
        pattern: str,
        origin: Endpoint | Fork | TypingCallable[[Request], Any],
    ) -> None:
        self._pattern = pattern
        self._origin = origin

    def matched(self) -> bool:
        return True

    def routes(self, prefix: str = "") -> tuple[RouteEntry, ...]:
        """Polymorphically produce route entries for this regex pattern."""
        combined = f"{prefix.rstrip('/')}/{self._pattern.lstrip('/')}"
        return EndpointRoutes(self._origin).routes(combined)

    async def route(self, request: Request) -> Endpoint:
        path = await request.path()
        match = re.match(self._pattern, path)
        if match:
            endpoint = await SourceEndpoint(self._origin).route(request)
            if endpoint.matched():
                params = match.groupdict()
                return WithParams(endpoint, params) if params else endpoint
        return MissingEndpoint()

