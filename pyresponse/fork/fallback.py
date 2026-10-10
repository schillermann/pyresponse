"""Fallback routing fork decorator in Pure OOP."""

from typing import Any, Callable

from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.source_endpoint import SourceEndpoint
from pyresponse.fork.fork import Fork
from pyresponse.request.request import Request
from pyresponse.response.response import Response


class Fallback(Fork):
    """Route fork delegating to a fallback endpoint if origin fork does not match."""

    def __init__(
        self,
        origin: Endpoint | Fork | Callable[[Request], Any],
        fallback: Endpoint | Callable[[Request], Any],
    ) -> None:
        self._origin = origin
        self._fallback = fallback

    def matched(self) -> bool:
        return True

    async def route(self, request: Request) -> Endpoint:
        matched = await SourceEndpoint(self._origin).route(request)
        if matched.matched():
            return matched
        return await SourceEndpoint(self._fallback).route(request)

    async def response(self, request: Request) -> Response:
        matched = await self.route(request)
        return await matched.response(request)
